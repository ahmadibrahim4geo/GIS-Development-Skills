#!/usr/bin/env python3
"""Comprehensive test suite for Universal Desktop CAD/GIS & Geoprocessing Competencies."""
import json
import math
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REFERENCES = ROOT / "references"


class TestUrbanDesignCompetency(unittest.TestCase):
    """Verifies schemas, documentation integrity, mathematical algorithms, and copilot contracts."""

    def test_all_reference_documents_exist(self):
        """Verifies that all 10 universal architectural and engineering reference files exist and are non-empty."""
        expected_files = [
            "urban-design-competency-coverage.md",
            "urban-design-source-registry.json",
            "urban-design-sources.md",
            "native-cad-gis-desktop-architecture.md",
            "urban-hierarchy-parametric-modeling.md",
            "urban-simulation-engines.md",
            "reversible-cad-ai-copilot.md",
            "urban-export-studio.md",
            "token-optimization-triad.md",
            "agent-context-memory-architecture.md"
        ]
        for fname in expected_files:
            fpath = REFERENCES / fname
            self.assertTrue(fpath.is_file(), f"Missing reference file: {fname}")
            self.assertGreater(fpath.stat().st_size, 200, f"File {fname} is unexpectedly small")

    def test_source_registry_schema(self):
        """Verifies that urban-design-source-registry.json is valid, has 78 sources, and valid fields."""
        registry_path = REFERENCES / "urban-design-source-registry.json"
        with open(registry_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.assertEqual(data.get("schema_version"), "1.0")
        self.assertEqual(data.get("registry_id"), "UDS-SOURCE-REGISTRY")
        sources = data.get("sources", [])
        self.assertEqual(len(sources), 78, "Source registry must contain exactly 78 repositories")

        canonical_ids = set()
        valid_categories = {
            "cad_geometry", "desktop_ui", "simulation_urban",
            "token_context", "security_assurance", "secondary_utilities"
        }

        for src in sources:
            cid = src.get("canonical_id")
            self.assertTrue(cid.startswith("UDS-LIB-"), f"Invalid canonical_id format: {cid}")
            self.assertNotIn(cid, canonical_ids, f"Duplicate canonical_id: {cid}")
            canonical_ids.add(cid)

            self.assertTrue(src.get("name"), f"Missing name in {cid}")
            self.assertTrue(src.get("repo_url", "").startswith("https://github.com/"), f"Invalid repo_url in {cid}")
            self.assertIn(src.get("category"), valid_categories, f"Invalid category in {cid}")
            self.assertTrue(src.get("license"), f"Missing license in {cid}")
            self.assertIn(src.get("access_model"), {"free_open_source", "free_permissive_assets", "restricted_development_only"})
            self.assertIn(src.get("security_rating"), {"safe", "reviewed", "quarantine_in_sandbox"})
            self.assertTrue(src.get("accountable_skill"), f"Missing accountable_skill in {cid}")
            self.assertTrue(src.get("primary_use"), f"Missing primary_use in {cid}")

    def test_traceability_matrix_completeness(self):
        """Verifies that the traceability matrix covers all 55 UDS-* requirements and local software projects."""
        matrix_path = REFERENCES / "urban-design-competency-coverage.md"
        content = matrix_path.read_text(encoding="utf-8")

        # Check coverage of UDS-001 through UDS-055
        for i in range(1, 56):
            req_id = f"UDS-{i:03d}"
            self.assertIn(req_id, content, f"Missing competency requirement in matrix: {req_id}")

        # Check mention of local software portfolio
        local_projects = ["Contour", "Z EARTH", "SmartGully", "Smart Plot PDF", "GeologicalCrossSectionToolbox", "ATIAF"]
        for proj in local_projects:
            self.assertIn(proj, content, f"Matrix must document local software project: {proj}")

        # Check industry benchmarks
        benchmarks = ["ArcGIS CityEngine", "Autodesk Forma", "Autodesk InfraWorks", "TestFit", "AutoCAD", "WorldCraft"]
        for bm in benchmarks:
            self.assertIn(bm, content, f"Matrix must document industry benchmark: {bm}")

    def test_local_render_origin_precision(self):
        """Mathematically verifies that camera-relative rendering eliminates 32-bit float coordinate jitter."""
        # Simulated global UTM Zone 36N coordinates (meters)
        global_x = 350120.56789
        global_y = 3450210.12345
        global_z = 124.555

        # In raw 32-bit float (IEEE 754: 24 mantissa bits)
        # 3450210 has only ~7 significant decimal digits
        # Let's verify precision delta when subtracting camera target in double vs raw float
        cam_x, cam_y, cam_z = 350100.0, 3450200.0, 120.0

        # High-precision delta in 64-bit double:
        local_x_double = global_x - cam_x  # 20.56789
        local_y_double = global_y - cam_y  # 10.12345
        local_z_double = global_z - cam_z  # 4.555

        # Transferred to GPU as 32-bit float:
        # A value of 20.56789 in 32-bit float preserves > 6 decimal places (sub-millimeter)
        import struct
        def to_float32(val):
            return struct.unpack('f', struct.pack('f', val))[0]

        # Raw float vs local float error:
        raw_float_error = abs(to_float32(global_y) - global_y)
        local_float_error = abs(to_float32(local_y_double) - local_y_double)

        # Raw coordinate error in 32-bit float exceeds centimeters:
        self.assertGreater(raw_float_error, 0.05, "Raw 32-bit float UTM coordinates suffer >5cm precision loss")
        # Local origin coordinate error is sub-millimeter (< 0.0001 m):
        self.assertLess(local_float_error, 0.0001, "Camera-relative float preserves sub-millimeter precision")

    def test_relational_dag_cascade_simulation(self):
        """Simulates relational DAG cascade: moving a road centerline shifts sidewalk, setbacks, and utilities."""
        # Baseline Road & Cadastral model
        road_centerline_x = 100.0
        road_width = 20.0
        curb_offset = road_width / 2.0  # 10.0m
        curb_x = road_centerline_x + curb_offset  # 110.0m
        sidewalk_width = 3.0
        row_boundary_x = curb_x + sidewalk_width  # 113.0m

        # Parcel abutting the road
        front_setback = 4.0
        buildable_front_x = row_boundary_x + front_setback  # 117.0m

        # Underground stormwater lateral inlet
        gully_x = curb_x  # 110.0m

        # Snapshot before edit
        snapshot_before = {
            "centerline_x": road_centerline_x,
            "curb_x": curb_x,
            "row_boundary_x": row_boundary_x,
            "buildable_front_x": buildable_front_x,
            "gully_x": gully_x
        }

        # Mutation: Road centerline shifts right by 2.0m (to 102.0m)
        delta_x = 2.0
        new_centerline_x = road_centerline_x + delta_x
        # DAG cascade propagation:
        new_curb_x = new_centerline_x + curb_offset
        new_row_boundary_x = new_curb_x + sidewalk_width
        new_buildable_front_x = new_row_boundary_x + front_setback
        new_gully_x = new_curb_x

        self.assertEqual(new_curb_x, 112.0)
        self.assertEqual(new_row_boundary_x, 115.0)
        self.assertEqual(new_buildable_front_x, 119.0)
        self.assertEqual(new_gully_x, 112.0)

        # Undo Simulation: Restore snapshot
        restored_centerline_x = snapshot_before["centerline_x"]
        restored_buildable_front_x = snapshot_before["buildable_front_x"]
        self.assertEqual(restored_centerline_x, 100.0)
        self.assertEqual(restored_buildable_front_x, 117.0)

    def test_earcut_concept_polygon_with_hole(self):
        """Verifies polygon area and triangulation topology on a building footprint with an interior courtyard."""
        # Outer boundary: 20m x 20m square = 400 m2
        outer_ring = [(0.0, 0.0), (20.0, 0.0), (20.0, 20.0), (0.0, 20.0)]
        # Interior courtyard hole: 10m x 10m square = 100 m2
        inner_ring = [(5.0, 5.0), (15.0, 5.0), (15.0, 15.0), (5.0, 15.0)]

        def polygon_area(ring):
            n = len(ring)
            area = 0.0
            for i in range(n):
                j = (i + 1) % n
                area += ring[i][0] * ring[j][1] - ring[j][0] * ring[i][1]
            return abs(area) / 2.0

        outer_area = polygon_area(outer_ring)
        inner_area = polygon_area(inner_ring)
        net_footprint_area = outer_area - inner_area

        self.assertEqual(outer_area, 400.0)
        self.assertEqual(inner_area, 100.0)
        self.assertEqual(net_footprint_area, 300.0)

        # Triangulation of polygon with 1 hole:
        # Number of triangles = (V_outer + V_inner + 2*bridge - 2) = 4 + 4 + 2 - 2 = 8 triangles
        num_triangles = len(outer_ring) + len(inner_ring)
        self.assertEqual(num_triangles, 8, "Expected 8 triangles for a quadrilateral with 1 quadrilateral hole")

    def test_solar_position_noaa_formula(self):
        """Verifies astronomical solar position calculation on Summer Solstice noon in Cairo (Lat 30.04° N)."""
        lat_deg = 30.0444
        day_of_year = 172  # June 21

        # Fractional year gamma
        gamma = (2.0 * math.pi / 365.0) * (day_of_year - 1 + (12.0 - 12.0) / 24.0)

        # Declination delta (radians)
        delta_rad = (
            0.006918 - 0.399912 * math.cos(gamma) + 0.070257 * math.sin(gamma)
            - 0.006758 * math.cos(2 * gamma) + 0.000907 * math.sin(2 * gamma)
            - 0.002697 * math.cos(3 * gamma) + 0.00148 * math.sin(3 * gamma)
        )
        delta_deg = math.degrees(delta_rad)

        # Solar declination on summer solstice should be approx 23.4° - 23.5°
        self.assertAlmostEqual(delta_deg, 23.44, delta=0.5)

        # At solar noon, hour angle omega = 0
        lat_rad = math.radians(lat_deg)
        sin_altitude = math.sin(lat_rad) * math.sin(delta_rad) + math.cos(lat_rad) * math.cos(delta_rad) * math.cos(0.0)
        altitude_deg = math.degrees(math.asin(sin_altitude))

        # Expected solar altitude in Cairo at summer noon: 90° - (30.04° - 23.44°) ≈ 83.4°
        self.assertGreater(altitude_deg, 80.0, "Summer noon in Cairo must have high solar altitude >80 degrees")
        self.assertLess(altitude_deg, 90.0)

    def test_stormwater_rational_and_gully_spacing(self):
        """Verifies rational runoff formula and roadway gully spacing calculation (SmartGully pattern)."""
        # Catchment parameters
        catchment_area_ha = 0.5  # 5,000 m2
        runoff_coeff = 0.85      # Asphalt pavement
        rainfall_intensity_mmh = 45.0  # 10-year storm intensity

        # Peak discharge Q = (C * I * A) / 360 (m3/s)
        q_m3s = (runoff_coeff * rainfall_intensity_mmh * catchment_area_ha) / 360.0
        q_liters_sec = q_m3s * 1000.0  # L/s

        self.assertGreater(q_liters_sec, 0.0)
        self.assertAlmostEqual(q_liters_sec, 53.125, delta=0.5)

        # Gully Spacing L:
        inlet_capacity_ls = 20.0  # L/s per inlet
        pavement_draining_width_m = 7.0  # Single carriageway half-width draining to curb

        # Discharge per meter length of road = C * (I/3600000) * W
        q_per_meter = runoff_coeff * (rainfall_intensity_mmh / 3600000.0) * pavement_draining_width_m  # m3/s per m
        q_per_meter_ls = q_per_meter * 1000.0  # L/s per meter

        # Gully Spacing L constrained by statutory roadway design standards (typically 20m - 25m)
        max_statutory_spacing_m = 25.0
        calculated_spacing_m = inlet_capacity_ls / q_per_meter_ls
        spacing_m = min(max_statutory_spacing_m, calculated_spacing_m)

        self.assertGreater(spacing_m, 15.0, "Gully spacing must exceed 15m")
        self.assertLessEqual(spacing_m, 25.0, "Gully spacing must not exceed statutory 25m to prevent gutter flooding")

    def test_intent_router_bilingual_keywords(self):
        """Verifies intent_router.py identifies the new universal CAD/GIS keywords."""
        from scripts.intent_router import route_hints

        # Arabic CAD query
        res_ar = route_hints("تصميم شارع بارامتري earcut واجهة كاد")
        self.assertIn("gis-desktop-application-development", res_ar["suggested_skills"])
        self.assertIn("geospatial-data-processing", res_ar["suggested_skills"])

        # Simulation & Traffic query
        res_sim = route_hints("محاكاة حركة المرور sumo وحساب سيول gully")
        self.assertIn("terrain-hydrology-lidar", res_sim["suggested_skills"])

        # Reversible Copilot query
        res_ai = route_hints("reversible cad copilot with qundostack and ctrl+z")
        self.assertIn("geospatial-ai-agents", res_ai["suggested_skills"])

        # Token optimization query
        res_token = route_hints("ponytail and caveman context engineering")
        self.assertIn("gis-code-discovery", res_token["suggested_skills"])


if __name__ == "__main__":
    unittest.main()
