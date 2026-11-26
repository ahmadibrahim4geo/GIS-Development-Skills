#!/usr/bin/env python3
"""Runnable T1 GNSS + SQLite + GPX 1.1 roundtrip contract demonstration for MOB-08."""
from pathlib import Path
import sys
import tempfile

SHARED_DIR = Path(__file__).resolve().parents[2] / "shared"
sys.path.insert(0, str(SHARED_DIR))
import mobile_field_core as core  # noqa: E402


def main() -> int:
    gnss = core.evaluate_location_capture(
        "allow_precise",
        source="external_ble_gnss",
        lat=30.0444,
        lon=31.2357,
        ellipsoidal_z_m=42.65,
        geoid_undulation_m=15.15,
        horizontal_accuracy_m=0.02,
        fix_timestamp_utc="2026-11-25T20:00:00Z",
        now_utc="2026-11-25T20:00:03Z",
        rtk_state="RTK_FIXED",
        rtk_correction_age_s=1.5,
        checkpoint_verified=True,
    )
    with tempfile.TemporaryDirectory() as tmp:
        db_path = Path(tmp) / "gnss_log.sqlite"
        out_gpx = Path(tmp) / "track.gpx"
        store = core.DurableFieldStore(db_path)
        store.save_edit(
            project_id="mob-08-gnss",
            layer_id="gnss_waypoints",
            feature_id="wp-cairo-01",
            op_id="op-mob08-1",
            base_revision=None,
            geometry={"type": "Point", "coordinates": [gnss["lon"], gnss["lat"]]},
            attributes={"name": "نقطة رصد RTK القاهرة"},
            crs=gnss["crs"],
            client_timestamp=gnss["fix_timestamp_utc"],
            device_id="demo-device-01",
            vertical_datum=gnss["height_datum"],
            elevation_m=gnss["orthometric_z_m"],
        )
        store.close()
        core.export_gpx_atomic(db_path, out_gpx)
        print("GNSS MOB-08 T1 OK:", gnss["height_datum"], gnss["orthometric_z_m"], "gpx_bytes=", out_gpx.stat().st_size)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
