#!/usr/bin/env python3
"""Deterministic SQLite-backed Mobile Field GIS Core (T1/T2 offline contract engine).

Implements durable WAL SQLite persistence across cold restarts, schema migration v1->v2,
the 15-field REQ-WM-042 outbox contract, GNSS/RTK provenance & GIS-015 vertical datum checks,
EXIF GPS stripping, OSM bulk-scrape blocking, BiDi RTL coordinate isolation, and atomic
GeoJSON + GPX 1.1 exports for independent verification.

NOT a compiled Android/iOS binary; native Android/iOS T3-T4 acceptance requires target SDKs/devices.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import sqlite3
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional
import xml.etree.ElementTree as ET

SYNC_15_FIELDS = (
    "project_id",
    "layer_id",
    "feature_id",
    "op_id",
    "base_revision",
    "geometry",
    "attributes",
    "crs",
    "client_timestamp",
    "server_timestamp",
    "device_id",
    "attachment_manifest",
    "deletion_tombstone",
    "checksum",
    "sync_state",
)

UTC_ISO_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z$")
OSM_SCRAPE_RE = re.compile(r"https?://(?:[a-c]\.)?tile\.openstreetmap\.org/\d+/\d+/\d+", re.IGNORECASE)
VALID_PERMISSION_MODES = {"allow_precise", "allow_approximate", "deny", "ask_later"}
VALID_HEIGHT_DATUMS = {"ellipsoidal_wgs84", "orthometric_egm2008", "orthometric_msl"}
VALID_RTK_STATES = {"NONE", "SINGLE", "DGPS", "RTK_FLOAT", "RTK_FIXED"}


def compute_op_checksum(
    feature_id: str,
    layer_id: str,
    geometry: Dict[str, Any],
    attributes: Dict[str, Any],
    crs: str,
    deletion_tombstone: bool,
) -> str:
    """Return deterministic SHA-256 checksum binding operation identity to its spatial payload."""
    canonical = json.dumps(
        {
            "feature_id": feature_id,
            "layer_id": layer_id,
            "geometry": geometry,
            "attributes": attributes,
            "crs": crs,
            "deletion_tombstone": bool(deletion_tombstone),
        },
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def format_bidi_coordinate_label(arabic_label: str, lat: float, lon: float, accuracy_m: Optional[float] = None) -> str:
    """Wrap numeric coordinates and accuracy in Unicode LRI..PDI isolates for safe RTL UI rendering."""
    acc_part = f" (±{accuracy_m:.1f} m)" if accuracy_m is not None else ""
    coord_ltr = f"\u2066{lat:.6f}, {lon:.6f} [EPSG:4326]{acc_part}\u2069"
    return f"{arabic_label}: {coord_ltr}"


def check_touch_target_dp(width_dp: float, height_dp: float, platform: str = "android") -> Dict[str, Any]:
    """Enforce >=48dp on Android and >=44pt on iOS accessibility touch target minimums."""
    min_size = 44.0 if platform == "ios" else 48.0
    ok = width_dp >= min_size and height_dp >= min_size
    return {"platform": platform, "min_required": min_size, "ok": ok}


def evaluate_tile_pack_source(url: str, *, attribution: str, license_ok: bool) -> None:
    """Reject bulk scraping of tile.openstreetmap.org or unattributed offline caches (MOB-QA-20)."""
    if OSM_SCRAPE_RE.search(url or ""):
        raise PermissionError("OSM tile server policy ban: bulk prefetch/caching of tile.openstreetmap.org is prohibited")
    if not license_ok or not isinstance(attribution, str) or not attribution.strip():
        raise PermissionError("Offline tile pack requires explicit redistribution permission and visible attribution")


def evaluate_location_capture(
    permission_mode: str,
    *,
    source: str,
    lat: Optional[float] = None,
    lon: Optional[float] = None,
    ellipsoidal_z_m: Optional[float] = None,
    geoid_undulation_m: Optional[float] = None,
    horizontal_accuracy_m: Optional[float] = None,
    fix_timestamp_utc: Optional[str] = None,
    now_utc: Optional[str] = None,
    max_age_s: float = 15.0,
    is_mock: bool = False,
    rtk_state: str = "NONE",
    rtk_correction_age_s: Optional[float] = None,
    checkpoint_verified: bool = False,
    manual_lat: Optional[float] = None,
    manual_lon: Optional[float] = None,
) -> Dict[str, Any]:
    """Normalize GNSS provenance, permission denials, mock flags, RTK claims, and Z datum (GIS-015)."""
    if permission_mode not in VALID_PERMISSION_MODES:
        raise ValueError(f"Unsupported permission_mode: {permission_mode}")

    if permission_mode in {"deny", "ask_later"}:
        if manual_lat is None or manual_lon is None:
            return {
                "status": "LOCATION_DENIED_AWAITING_MANUAL",
                "source": "none",
                "manual_fallback_ready": True,
                "stale": False,
                "is_cm_verified": False,
            }
        return {
            "status": "MANUAL_FALLBACK_ACTIVE",
            "source": "manual_map_tap",
            "lat": float(manual_lat),
            "lon": float(manual_lon),
            "crs": "EPSG:4326",
            "height_datum": None,
            "horizontal_accuracy_m": None,
            "stale": False,
            "is_cm_verified": False,
        }

    if lat is None or lon is None:
        raise ValueError("Granted location mode requires lat and lon")
    if not fix_timestamp_utc or not UTC_ISO_RE.match(fix_timestamp_utc):
        raise ValueError("fix_timestamp_utc must be strict ISO-8601 UTC (...Z)")
    if rtk_state not in VALID_RTK_STATES:
        raise ValueError(f"Invalid rtk_state: {rtk_state}")

    fix_dt = datetime.fromisoformat(fix_timestamp_utc.replace("Z", "+00:00"))
    ref_dt = (
        datetime.fromisoformat(now_utc.replace("Z", "+00:00"))
        if now_utc
        else datetime.now(timezone.utc)
    )
    fix_age_s = max(0.0, (ref_dt - fix_dt).total_seconds())
    stale = fix_age_s > max_age_s

    orthometric_z_m = None
    height_datum = None
    if ellipsoidal_z_m is not None:
        height_datum = "ellipsoidal_wgs84"
        if geoid_undulation_m is not None:
            orthometric_z_m = round(float(ellipsoidal_z_m) - float(geoid_undulation_m), 4)
            height_datum = "orthometric_egm2008"

    is_cm_verified = (
        not is_mock
        and not stale
        and source in {"external_ble_gnss", "external_usb_rtk"}
        and rtk_state == "RTK_FIXED"
        and rtk_correction_age_s is not None
        and rtk_correction_age_s <= 5.0
        and horizontal_accuracy_m is not None
        and horizontal_accuracy_m <= 0.05
        and bool(checkpoint_verified)
    )

    warnings: List[str] = []
    if is_mock:
        warnings.append("MOCK_PROVIDER_DETECTED")
    if stale:
        warnings.append(f"STALE_FIX_{fix_age_s:.1f}s")
    if permission_mode == "allow_approximate":
        warnings.append("APPROXIMATE_LOCATION_ONLY")
    if rtk_state == "RTK_FLOAT":
        warnings.append("RTK_FLOAT_NOT_CENTIMETER_FIXED")

    return {
        "status": "MOCK_BLOCKED" if is_mock else ("STALE_FIX" if stale else "FIX_RECORDED"),
        "source": source,
        "lat": float(lat),
        "lon": float(lon),
        "crs": "EPSG:4326",
        "ellipsoidal_z_m": float(ellipsoidal_z_m) if ellipsoidal_z_m is not None else None,
        "geoid_undulation_m": float(geoid_undulation_m) if geoid_undulation_m is not None else None,
        "orthometric_z_m": orthometric_z_m,
        "height_datum": height_datum,
        "horizontal_accuracy_m": float(horizontal_accuracy_m) if horizontal_accuracy_m is not None else None,
        "fix_timestamp_utc": fix_timestamp_utc,
        "fix_age_s": round(fix_age_s, 3),
        "stale": stale,
        "is_mock": is_mock,
        "rtk_state": rtk_state,
        "is_cm_verified": is_cm_verified,
        "warnings": warnings,
    }


def sanitize_photo_attachment(
    metadata: Dict[str, Any],
    image_bytes: bytes,
    *,
    strip_exif_gps: bool = True,
    explicit_gps_opt_in: bool = False,
) -> Dict[str, Any]:
    """Strip sensitive EXIF GPS tags by default unless user explicitly opted in (MOB-QA-10)."""
    clean_meta = deepcopy(metadata)
    gps_keys = ("GPSLatitude", "GPSLongitude", "GPSAltitude", "GPSTimeStamp", "GPSImgDirection")
    stripped = False
    if strip_exif_gps and not explicit_gps_opt_in:
        for key in gps_keys:
            if key in clean_meta:
                clean_meta.pop(key, None)
                stripped = True
    return {
        "sha256": hashlib.sha256(image_bytes).hexdigest(),
        "byte_size": len(image_bytes),
        "exif_gps_stripped": stripped,
        "metadata": clean_meta,
    }


class DurableFieldStore:
    """SQLite-backed offline vector & 15-field outbox store surviving restart and schema upgrade."""

    def __init__(self, db_path: Path, *, min_free_bytes: int = 10 * 1024 * 1024, simulated_free_bytes: Optional[int] = None):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.min_free_bytes = min_free_bytes
        self.simulated_free_bytes = simulated_free_bytes
        self.conn = sqlite3.connect(str(self.db_path))
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA journal_mode=WAL;")
        self.conn.execute("PRAGMA foreign_keys=ON;")
        self._init_schema_v2()

    def _init_schema_v2(self) -> None:
        with self.conn:
            self.conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS meta (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS features (
                    feature_id TEXT PRIMARY KEY,
                    project_id TEXT NOT NULL,
                    layer_id TEXT NOT NULL,
                    geometry_json TEXT NOT NULL,
                    attributes_json TEXT NOT NULL,
                    crs TEXT NOT NULL,
                    vertical_datum TEXT,
                    elevation_m REAL,
                    captured_at_utc TEXT NOT NULL,
                    server_revision INTEGER,
                    deletion_tombstone INTEGER NOT NULL DEFAULT 0
                );
                CREATE TABLE IF NOT EXISTS outbox (
                    op_id TEXT PRIMARY KEY,
                    project_id TEXT NOT NULL,
                    layer_id TEXT NOT NULL,
                    feature_id TEXT NOT NULL,
                    base_revision INTEGER,
                    geometry_json TEXT NOT NULL,
                    attributes_json TEXT NOT NULL,
                    crs TEXT NOT NULL,
                    client_timestamp TEXT NOT NULL,
                    server_timestamp TEXT,
                    device_id TEXT NOT NULL,
                    attachment_manifest_json TEXT NOT NULL,
                    deletion_tombstone INTEGER NOT NULL DEFAULT 0,
                    checksum TEXT NOT NULL,
                    sync_state TEXT NOT NULL,
                    server_record_json TEXT
                );
                """
            )
            cur = self.conn.execute("SELECT value FROM meta WHERE key='schema_version'").fetchone()
            if cur is None:
                self.conn.execute("INSERT INTO meta(key, value) VALUES('schema_version', '2')")

    def close(self) -> None:
        self.conn.close()

    def check_storage_quota(self, incoming_bytes: int = 0) -> None:
        """Abort writes cleanly before disk exhaustion corrupts SQLite/GeoPackage state (MOB-QA-09)."""
        if self.simulated_free_bytes is not None and (self.simulated_free_bytes - incoming_bytes) < self.min_free_bytes:
            raise OSError("Insufficient storage quota: write aborted cleanly without DB corruption")

    def save_edit(
        self,
        *,
        project_id: str,
        layer_id: str,
        feature_id: str,
        op_id: str,
        base_revision: Optional[int],
        geometry: Dict[str, Any],
        attributes: Dict[str, Any],
        crs: str = "EPSG:4326",
        client_timestamp: str,
        device_id: str,
        attachment_manifest: Optional[List[Dict[str, Any]]] = None,
        deletion_tombstone: bool = False,
        vertical_datum: Optional[str] = None,
        elevation_m: Optional[float] = None,
        estimated_bytes: int = 1024,
    ) -> Dict[str, Any]:
        """Atomically persist feature state and 15-field outbox entry inside one SQLite transaction."""
        if not UTC_ISO_RE.match(client_timestamp):
            raise ValueError("client_timestamp must be UTC ISO-8601 (...Z)")
        if vertical_datum is not None and vertical_datum not in VALID_HEIGHT_DATUMS:
            raise ValueError(f"Unsupported vertical_datum: {vertical_datum}")
        self.check_storage_quota(estimated_bytes)

        attachments = attachment_manifest or []
        checksum = compute_op_checksum(feature_id, layer_id, geometry, attributes, crs, deletion_tombstone)
        geom_json = json.dumps(geometry, ensure_ascii=False)
        attr_json = json.dumps(attributes, ensure_ascii=False)
        att_json = json.dumps(attachments, ensure_ascii=False)

        with self.conn:
            self.conn.execute(
                """
                INSERT INTO features(feature_id, project_id, layer_id, geometry_json, attributes_json, crs,
                                     vertical_datum, elevation_m, captured_at_utc, server_revision, deletion_tombstone)
                VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(feature_id) DO UPDATE SET
                    geometry_json=excluded.geometry_json,
                    attributes_json=excluded.attributes_json,
                    crs=excluded.crs,
                    vertical_datum=excluded.vertical_datum,
                    elevation_m=excluded.elevation_m,
                    captured_at_utc=excluded.captured_at_utc,
                    deletion_tombstone=excluded.deletion_tombstone
                """,
                (
                    feature_id, project_id, layer_id, geom_json, attr_json, crs,
                    vertical_datum, elevation_m, client_timestamp, base_revision, 1 if deletion_tombstone else 0,
                ),
            )
            self.conn.execute(
                """
                INSERT INTO outbox(op_id, project_id, layer_id, feature_id, base_revision, geometry_json,
                                   attributes_json, crs, client_timestamp, server_timestamp, device_id,
                                   attachment_manifest_json, deletion_tombstone, checksum, sync_state, server_record_json)
                VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, NULL, ?, ?, ?, ?, 'PENDING', NULL)
                """,
                (
                    op_id, project_id, layer_id, feature_id, base_revision, geom_json, attr_json, crs,
                    client_timestamp, device_id, att_json, 1 if deletion_tombstone else 0, checksum,
                ),
            )

        return {
            "project_id": project_id,
            "layer_id": layer_id,
            "feature_id": feature_id,
            "op_id": op_id,
            "base_revision": base_revision,
            "geometry": geometry,
            "attributes": attributes,
            "crs": crs,
            "client_timestamp": client_timestamp,
            "server_timestamp": None,
            "device_id": device_id,
            "attachment_manifest": attachments,
            "deletion_tombstone": bool(deletion_tombstone),
            "checksum": checksum,
            "sync_state": "PENDING",
        }

    def list_outbox(self, state: Optional[str] = None) -> List[Dict[str, Any]]:
        sql = "SELECT * FROM outbox"
        params: tuple[Any, ...] = ()
        if state is not None:
            sql += " WHERE sync_state=?"
            params = (state,)
        rows = self.conn.execute(sql + " ORDER BY rowid ASC", params).fetchall()
        out = []
        for r in rows:
            out.append(
                {
                    "project_id": r["project_id"],
                    "layer_id": r["layer_id"],
                    "feature_id": r["feature_id"],
                    "op_id": r["op_id"],
                    "base_revision": r["base_revision"],
                    "geometry": json.loads(r["geometry_json"]),
                    "attributes": json.loads(r["attributes_json"]),
                    "crs": r["crs"],
                    "client_timestamp": r["client_timestamp"],
                    "server_timestamp": r["server_timestamp"],
                    "device_id": r["device_id"],
                    "attachment_manifest": json.loads(r["attachment_manifest_json"]),
                    "deletion_tombstone": bool(r["deletion_tombstone"]),
                    "checksum": r["checksum"],
                    "sync_state": r["sync_state"],
                    "server_record": json.loads(r["server_record_json"]) if r["server_record_json"] else None,
                }
            )
        return out

    def flush(self, server: "DurableMockSyncServer", *, connected: bool, auth_status: int = 200) -> Dict[str, int]:
        """Flush PENDING/BLOCKED outbox items with idempotency, 401/403 pause, and conflict retention."""
        acked = 0
        conflicts = 0
        blocked = 0
        for row in self.list_outbox():
            if row["sync_state"] not in {"PENDING", "BLOCKED"}:
                continue
            if not connected or auth_status in {401, 403}:
                with self.conn:
                    self.conn.execute("UPDATE outbox SET sync_state='BLOCKED' WHERE op_id=?", (row["op_id"],))
                blocked += 1
                continue
            resp = server.submit(row)
            with self.conn:
                if resp["status"] == "ACKED":
                    self.conn.execute(
                        "UPDATE outbox SET sync_state='ACKED', server_timestamp=? WHERE op_id=?",
                        (resp["server_timestamp"], row["op_id"]),
                    )
                    self.conn.execute(
                        "UPDATE features SET server_revision=? WHERE feature_id=?",
                        (resp["server_revision"], row["feature_id"]),
                    )
                    acked += 1
                elif resp["status"] == "CONFLICT":
                    self.conn.execute(
                        "UPDATE outbox SET sync_state='CONFLICT', server_record_json=? WHERE op_id=?",
                        (json.dumps(resp["server_record"], ensure_ascii=False), row["op_id"]),
                    )
                    conflicts += 1
        return {"acked": acked, "conflicts": conflicts, "blocked": blocked}

    def list_features(self, *, include_deleted: bool = False) -> List[Dict[str, Any]]:
        sql = "SELECT * FROM features" if include_deleted else "SELECT * FROM features WHERE deletion_tombstone=0"
        rows = self.conn.execute(sql + " ORDER BY rowid ASC").fetchall()
        return [
            {
                "feature_id": r["feature_id"],
                "project_id": r["project_id"],
                "layer_id": r["layer_id"],
                "geometry": json.loads(r["geometry_json"]),
                "attributes": json.loads(r["attributes_json"]),
                "crs": r["crs"],
                "vertical_datum": r["vertical_datum"],
                "elevation_m": r["elevation_m"],
                "captured_at_utc": r["captured_at_utc"],
                "server_revision": r["server_revision"],
                "deletion_tombstone": bool(r["deletion_tombstone"]),
            }
            for r in rows
        ]


class DurableMockSyncServer:
    """In-memory deterministic server validating checksum idempotency and base_revision (no blind LWW)."""

    def __init__(self) -> None:
        self.records: Dict[str, Dict[str, Any]] = {}
        self.acked_ops: Dict[str, Dict[str, Any]] = {}

    def submit(self, op: Dict[str, Any], *, server_timestamp: str = "2026-11-25T20:10:00Z") -> Dict[str, Any]:
        op_id = op["op_id"]
        if op_id in self.acked_ops:
            prior = self.acked_ops[op_id]
            if prior["checksum"] != op["checksum"]:
                raise ValueError("op_id collision with altered payload checksum")
            return prior

        fid = op["feature_id"]
        current = self.records.get(fid)
        current_rev = current["server_revision"] if current else None
        if op["base_revision"] != current_rev:
            return {"status": "CONFLICT", "server_record": deepcopy(current)}

        next_rev = 1 if current_rev is None else current_rev + 1
        self.records[fid] = {
            "feature_id": fid,
            "server_revision": next_rev,
            "geometry": deepcopy(op["geometry"]),
            "attributes": deepcopy(op["attributes"]),
            "crs": op["crs"],
            "deleted": bool(op["deletion_tombstone"]),
            "device_id": op["device_id"],
        }
        receipt = {
            "status": "ACKED",
            "server_revision": next_rev,
            "server_timestamp": server_timestamp,
            "checksum": op["checksum"],
        }
        self.acked_ops[op_id] = receipt
        return receipt


def upgrade_v1_db_to_v2(db_path: Path) -> int:
    """Migrate a v1 mobile SQLite table cleanly to v2 schema without losing existing field records."""
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT feature_id, name, lon, lat FROM features_v1").fetchall()
    conn.close()

    store = DurableFieldStore(db_path)
    migrated = 0
    for r in rows:
        store.save_edit(
            project_id="migrated-v1",
            layer_id="field_points",
            feature_id=r["feature_id"],
            op_id=f"mig-{r['feature_id']}",
            base_revision=None,
            geometry={"type": "Point", "coordinates": [r["lon"], r["lat"]]},
            attributes={"name": r["name"], "migrated_from": "v1"},
            crs="EPSG:4326",
            client_timestamp="2026-11-25T20:00:00Z",
            device_id="migration-worker",
        )
        migrated += 1
    with store.conn:
        store.conn.execute("UPDATE meta SET value='2' WHERE key='schema_version'")
    store.close()
    return migrated


def _atomic_write_text(path: Path, text: str) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp.write_text(text, encoding="utf-8")
    os.replace(tmp, path)


def export_geojson_atomic(db_path: Path, output_path: Path) -> Path:
    """Export active SQLite features atomically as RFC 7946 GeoJSON with vertical provenance."""
    store = DurableFieldStore(db_path)
    try:
        feats = []
        for row in store.list_features(include_deleted=False):
            props = deepcopy(row["attributes"])
            props["_crs"] = row["crs"]
            props["_vertical_datum"] = row["vertical_datum"]
            props["_elevation_m"] = row["elevation_m"]
            props["_captured_at_utc"] = row["captured_at_utc"]
            feats.append({"type": "Feature", "id": row["feature_id"], "geometry": row["geometry"], "properties": props})
        fc = {"type": "FeatureCollection", "features": feats}
        _atomic_write_text(output_path, json.dumps(fc, ensure_ascii=False, indent=2) + "\n")
    finally:
        store.close()
    return output_path


def export_gpx_atomic(db_path: Path, output_path: Path) -> Path:
    """Export Point features atomically as GPX 1.1 XML preserving UTF-8 Arabic names and Z metadata."""
    store = DurableFieldStore(db_path)
    try:
        gpx = ET.Element("gpx", {"version": "1.1", "creator": "GIS-Development-Skills-MobileCore"})
        for row in store.list_features(include_deleted=False):
            geom = row["geometry"]
            if geom.get("type") != "Point":
                continue
            coords = geom["coordinates"]
            wpt = ET.SubElement(gpx, "wpt", {"lat": str(coords[1]), "lon": str(coords[0])})
            if row["elevation_m"] is not None:
                ET.SubElement(wpt, "ele").text = str(row["elevation_m"])
            ET.SubElement(wpt, "time").text = row["captured_at_utc"]
            ET.SubElement(wpt, "name").text = str(row["attributes"].get("name") or row["feature_id"])
            if row["vertical_datum"]:
                ET.SubElement(wpt, "desc").text = f"datum={row['vertical_datum']}"
        xml_text = '<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(gpx, encoding="unicode") + "\n"
        _atomic_write_text(output_path, xml_text)
    finally:
        store.close()
    return output_path
