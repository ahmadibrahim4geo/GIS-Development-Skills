#!/usr/bin/env python3
"""Deterministic SQLite, GNSS/RTK, sync, privacy, and export contract tests for Mobile GIS (T1)."""

import json
import sqlite3
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SHARED_DIR = ROOT / "examples" / "mobile-gis" / "shared"
FIXTURES_DIR = ROOT / "tests" / "shared-gis-fixtures"

if str(SHARED_DIR) not in sys.path:
    sys.path.insert(0, str(SHARED_DIR))

import mobile_field_core as core  # noqa: E402


class MobileFieldContractTests(unittest.TestCase):
    """Verifies durable SQLite persistence, 15-field outbox, GNSS/Z-datum, privacy, and exports."""

    @classmethod
    def setUpClass(cls):
        cls.geojson = json.loads((FIXTURES_DIR / "geojson_epsg4326_bilingual.geojson").read_text(encoding="utf-8"))
        cls.contracts = json.loads((FIXTURES_DIR / "expected-shared-contracts.json").read_text(encoding="utf-8"))

    def test_sqlite_cold_restart_preserves_geojson_and_15_field_outbox(self):
        pt = self.geojson["features"][0]
        with tempfile.TemporaryDirectory() as tmp:
            db_path = Path(tmp) / "field.sqlite"
            store = core.DurableFieldStore(db_path)
            op = store.save_edit(
                project_id="cairo-field-01",
                layer_id="inspections",
                feature_id=pt["id"],
                op_id="op-mob-001",
                base_revision=None,
                geometry=pt["geometry"],
                attributes=pt["properties"],
                crs="EPSG:4326",
                client_timestamp="2026-11-25T20:00:00Z",
                device_id="pixel-field-hash-01",
                vertical_datum="orthometric_egm2008",
                elevation_m=27.5,
            )
            store.close()

            for req_field in core.SYNC_15_FIELDS:
                self.assertIn(req_field, op)

            reopened = core.DurableFieldStore(db_path)
            try:
                queued = reopened.list_outbox(state="PENDING")
                self.assertEqual(1, len(queued))
                self.assertEqual(pt["properties"]["name_ar"], queued[0]["attributes"]["name_ar"])
                self.assertIn("notes", queued[0]["attributes"])
                self.assertIsNone(queued[0]["attributes"]["notes"])
                self.assertEqual("PENDING", queued[0]["sync_state"])
            finally:
                reopened.close()

    def test_idempotent_retry_and_forged_payload_rejection(self):
        with tempfile.TemporaryDirectory() as tmp:
            db_path = Path(tmp) / "retry.sqlite"
            store = core.DurableFieldStore(db_path)
            server = core.DurableMockSyncServer()
            try:
                op = store.save_edit(
                    project_id="p1",
                    layer_id="l1",
                    feature_id="f-10",
                    op_id="op-idem-1",
                    base_revision=None,
                    geometry={"type": "Point", "coordinates": [31.2357, 30.0444]},
                    attributes={"name": "بئر مياه"},
                    client_timestamp="2026-11-25T20:01:00Z",
                    device_id="dev-a",
                )
                first = server.submit(op)
                second = server.submit(op)
                self.assertEqual(1, first["server_revision"])
                self.assertEqual(first, second)

                forged = dict(op)
                forged["attributes"] = {"name": "تعديل لاحق"}
                forged["checksum"] = core.compute_op_checksum(
                    "f-10", "l1", op["geometry"], forged["attributes"], "EPSG:4326", False
                )
                with self.assertRaises(ValueError):
                    server.submit(forged)
            finally:
                store.close()

    def test_conflict_blocks_blind_lww_and_401_pauses_without_drop(self):
        with tempfile.TemporaryDirectory() as tmp:
            store_a = core.DurableFieldStore(Path(tmp) / "dev_a.sqlite")
            store_b = core.DurableFieldStore(Path(tmp) / "dev_b.sqlite")
            server = core.DurableMockSyncServer()
            try:
                store_a.save_edit(
                    project_id="p1", layer_id="l1", feature_id="f-20", op_id="op-init",
                    base_revision=None, geometry={"type": "Point", "coordinates": [31.2, 30.0]},
                    attributes={"status": "initial"}, client_timestamp="2026-11-25T20:00:00Z", device_id="dev-a",
                )
                self.assertEqual(1, store_a.flush(server, connected=True, auth_status=200)["acked"])

                store_a.save_edit(
                    project_id="p1", layer_id="l1", feature_id="f-20", op_id="op-a-2",
                    base_revision=1, geometry={"type": "Point", "coordinates": [31.2, 30.0]},
                    attributes={"status": "device-a-updated"}, client_timestamp="2026-11-25T20:02:00Z", device_id="dev-a",
                )
                store_a.flush(server, connected=True, auth_status=200)

                store_b.save_edit(
                    project_id="p1", layer_id="l1", feature_id="f-20", op_id="op-b-stale",
                    base_revision=1, geometry={"type": "Point", "coordinates": [31.2, 30.0]},
                    attributes={"status": "device-b-stale"}, client_timestamp="2026-11-25T20:03:00Z", device_id="dev-b",
                )
                res_conflict = store_b.flush(server, connected=True, auth_status=200)
                self.assertEqual(1, res_conflict["conflicts"])
                self.assertEqual("device-a-updated", server.records["f-20"]["attributes"]["status"])
                conflicts = store_b.list_outbox(state="CONFLICT")
                self.assertEqual(1, len(conflicts))
                self.assertEqual("device-a-updated", conflicts[0]["server_record"]["attributes"]["status"])

                store_b.save_edit(
                    project_id="p1", layer_id="l1", feature_id="f-21", op_id="op-b-auth",
                    base_revision=None, geometry={"type": "Point", "coordinates": [31.3, 30.1]},
                    attributes={"status": "needs-auth"}, client_timestamp="2026-11-25T20:04:00Z", device_id="dev-b",
                )
                paused = store_b.flush(server, connected=True, auth_status=401)
                self.assertEqual(1, paused["blocked"])
                resumed = store_b.flush(server, connected=True, auth_status=200)
                self.assertEqual(1, resumed["acked"])
            finally:
                store_a.close()
                store_b.close()

    def test_low_storage_quota_prevents_sqlite_corruption(self):
        with tempfile.TemporaryDirectory() as tmp:
            db_path = Path(tmp) / "quota.sqlite"
            store = core.DurableFieldStore(db_path, min_free_bytes=10_000, simulated_free_bytes=5_000)
            try:
                with self.assertRaises(OSError):
                    store.save_edit(
                        project_id="p1", layer_id="l1", feature_id="f-disk", op_id="op-disk",
                        base_revision=None, geometry={"type": "Point", "coordinates": [31.2, 30.0]},
                        attributes={"name": "blocked"}, client_timestamp="2026-11-25T20:00:00Z", device_id="dev-q",
                    )
                self.assertEqual([], store.list_outbox())
            finally:
                store.close()

    def test_v1_to_v2_sqlite_schema_migration_preserves_records(self):
        with tempfile.TemporaryDirectory() as tmp:
            db_path = Path(tmp) / "upgrade.sqlite"
            conn = sqlite3.connect(str(db_path))
            with conn:
                conn.execute("CREATE TABLE features_v1 (feature_id TEXT PRIMARY KEY, name TEXT, lon REAL, lat REAL)")
                conn.execute("INSERT INTO features_v1 VALUES ('v1-01', 'عمود إنارة ٠١', 31.235, 30.044)")
            conn.close()

            migrated = core.upgrade_v1_db_to_v2(db_path)
            self.assertEqual(1, migrated)
            store = core.DurableFieldStore(db_path)
            try:
                feats = store.list_features()
                self.assertEqual(1, len(feats))
                self.assertEqual("عمود إنارة ٠١", feats[0]["attributes"]["name"])
            finally:
                store.close()

    def test_location_permission_deny_and_ask_later_manual_fallback(self):
        waiting = core.evaluate_location_capture("deny", source="fused_os")
        self.assertEqual("LOCATION_DENIED_AWAITING_MANUAL", waiting["status"])
        self.assertTrue(waiting["manual_fallback_ready"])

        manual = core.evaluate_location_capture("ask_later", source="fused_os", manual_lat=30.0444, manual_lon=31.2357)
        self.assertEqual("manual_map_tap", manual["source"])
        self.assertFalse(manual["is_cm_verified"])

    def test_gnss_vertical_datum_stale_mock_and_rtk_gates(self):
        z_ref = self.contracts["gis_015_vertical_datum_z_utc"]
        rtk = core.evaluate_location_capture(
            "allow_precise",
            source="external_ble_gnss",
            lat=30.0444,
            lon=31.2357,
            ellipsoidal_z_m=z_ref["ellipsoidal_height_m"],
            geoid_undulation_m=z_ref["geoid_undulation_egm2008_m"],
            horizontal_accuracy_m=0.018,
            fix_timestamp_utc="2026-11-25T20:00:00Z",
            now_utc="2026-11-25T20:00:02Z",
            rtk_state="RTK_FIXED",
            rtk_correction_age_s=1.0,
            checkpoint_verified=True,
        )
        self.assertAlmostEqual(z_ref["expected_orthometric_m"], rtk["orthometric_z_m"], delta=z_ref["tolerance_m"])
        self.assertEqual("orthometric_egm2008", rtk["height_datum"])
        self.assertRegex(rtk["fix_timestamp_utc"], z_ref["utc_timestamp_pattern"])
        self.assertTrue(rtk["is_cm_verified"])

        mock_fix = core.evaluate_location_capture(
            "allow_precise",
            source="external_ble_gnss",
            lat=30.0444,
            lon=31.2357,
            horizontal_accuracy_m=0.01,
            fix_timestamp_utc="2026-11-25T20:00:00Z",
            now_utc="2026-11-25T20:00:01Z",
            is_mock=True,
            rtk_state="RTK_FIXED",
            rtk_correction_age_s=1.0,
            checkpoint_verified=True,
        )
        self.assertEqual("MOCK_BLOCKED", mock_fix["status"])
        self.assertFalse(mock_fix["is_cm_verified"])

        stale_fix = core.evaluate_location_capture(
            "allow_precise",
            source="fused_os",
            lat=30.0,
            lon=31.2,
            horizontal_accuracy_m=6.0,
            fix_timestamp_utc="2026-11-25T19:58:00Z",
            now_utc="2026-11-25T20:00:00Z",
        )
        self.assertTrue(stale_fix["stale"])
        self.assertEqual("STALE_FIX", stale_fix["status"])

    def test_exif_gps_privacy_strip_and_osm_tile_ban(self):
        att = core.sanitize_photo_attachment(
            {"Model": "FieldCam", "GPSLatitude": 30.0444, "GPSLongitude": 31.2357},
            b"synthetic-jpeg-bytes",
        )
        self.assertTrue(att["exif_gps_stripped"])
        self.assertNotIn("GPSLatitude", att["metadata"])

        with self.assertRaises(PermissionError):
            core.evaluate_tile_pack_source(
                "https://tile.openstreetmap.org/12/2400/1680.png",
                attribution="© OpenStreetMap contributors",
                license_ok=True,
            )
        core.evaluate_tile_pack_source(
            "https://tiles.example.org/selfhosted-cairo.pmtiles",
            attribution="Self-hosted ODbL PMTiles",
            license_ok=True,
        )

    def test_bidi_rtl_coordinate_isolation_and_touch_targets(self):
        label = core.format_bidi_coordinate_label("موقع الرصد", 30.0444, 31.2357, 2.4)
        self.assertIn("\u206630.044400, 31.235700 [EPSG:4326] (±2.4 m)\u2069", label)
        self.assertTrue(core.check_touch_target_dp(48, 48, "android")["ok"])
        self.assertFalse(core.check_touch_target_dp(44, 44, "android")["ok"])
        self.assertTrue(core.check_touch_target_dp(44, 44, "ios")["ok"])

    def test_atomic_geojson_and_gpx_export_independent_readback(self):
        with tempfile.TemporaryDirectory() as tmp:
            db_path = Path(tmp) / "export.sqlite"
            gj_path = Path(tmp) / "out.geojson"
            gpx_path = Path(tmp) / "out.gpx"
            store = core.DurableFieldStore(db_path)
            try:
                store.save_edit(
                    project_id="p-exp",
                    layer_id="assets",
                    feature_id="pt-ar-01",
                    op_id="op-exp-1",
                    base_revision=None,
                    geometry={"type": "Point", "coordinates": [31.2357, 30.0444]},
                    attributes={"name": "محطة مياه النيل <شمال>", "note": None},
                    crs="EPSG:4326",
                    client_timestamp="2026-11-25T20:05:00Z",
                    device_id="dev-x",
                    vertical_datum="orthometric_egm2008",
                    elevation_m=27.5,
                )
            finally:
                store.close()

            core.export_geojson_atomic(db_path, gj_path)
            core.export_gpx_atomic(db_path, gpx_path)

            loaded_gj = json.loads(gj_path.read_text(encoding="utf-8"))
            self.assertEqual(1, len(loaded_gj["features"]))
            props = loaded_gj["features"][0]["properties"]
            self.assertEqual("محطة مياه النيل <شمال>", props["name"])
            self.assertIsNone(props["note"])
            self.assertEqual("orthometric_egm2008", props["_vertical_datum"])

            tree = ET.parse(gpx_path)
            wpt = tree.getroot().find("wpt")
            self.assertIsNotNone(wpt)
            self.assertEqual("30.0444", wpt.attrib["lat"])
            self.assertEqual("محطة مياه النيل <شمال>", wpt.find("name").text)
            self.assertEqual("27.5", wpt.find("ele").text)
            self.assertEqual("2026-11-25T20:05:00Z", wpt.find("time").text)


if __name__ == "__main__":
    unittest.main()
