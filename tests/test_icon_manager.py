"""Offline tests: unified GIS icon-source policies and NEW-only KMZ exporter."""
import importlib.util
from io import BytesIO
import json
from pathlib import Path
import struct
import unittest
import zlib
from xml.etree import ElementTree as ET
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "export_new_kmz", ROOT / "examples/icon-manager/export_new_kmz.py"
)
exporter = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(exporter)


def minimal_png():
    def chunk(kind, data):
        return (struct.pack(">I", len(data)) + kind + data +
                struct.pack(">I", zlib.crc32(kind + data) & 0xffffffff))
    header = struct.pack(">IIBBBBB", 1, 1, 8, 6, 0, 0, 0)
    pixels = zlib.compress(bytes((0, 216, 60, 60, 255)))
    return (exporter.PNG_SIGNATURE + chunk(b"IHDR", header) +
            chunk(b"IDAT", pixels) + chunk(b"IEND", b""))


class TestNewIconExport(unittest.TestCase):
    def test_kml_abgr_and_alpha(self):
        self.assertEqual(exporter.kml_abgr("#ff0000"), "ff0000ff")
        self.assertEqual(exporter.kml_abgr("#00FF00", 0), "0000ff00")
        self.assertEqual(exporter.kml_abgr("#112233", 1), "ff332211")
        self.assertEqual(exporter.kml_abgr("#FFFFFF"), "ffffffff")

    def test_invalid_color_and_coordinates(self):
        for color in ("red", "#FFF", "#FFZZ00", ""):
            with self.subTest(color=color), self.assertRaises(ValueError):
                exporter.kml_abgr(color)
        image = minimal_png()
        for kwargs in ({"lon": 181, "lat": 30}, {"lon": 31, "lat": -92},
                       {"lon": float("nan"), "lat": 30},
                       {"lon": 31, "lat": 30, "scale": 0}):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                exporter.kmz_bytes(image, "Location", **kwargs)

    def test_new_kmz_has_relative_png_href_and_source_bytes(self):
        image = minimal_png()
        package = exporter.kmz_bytes(image, "مطار & Place", 31.23, 30.05,
                                     "#c53748", 1, 1.25, 90,
                                     "Map icon created by user")
        with ZipFile(BytesIO(package)) as archive:
            self.assertEqual(set(archive.namelist()),
                             {"doc.kml", "files/icons/marker.png"})
            self.assertEqual(archive.read("files/icons/marker.png"), image)
            root = ET.fromstring(archive.read("doc.kml"))
            ns = {"k": "http://www.opengis.net/kml/2.2"}
            self.assertEqual(root.findtext(".//k:Placemark/k:name", namespaces=ns),
                             "مطار & Place")
            self.assertEqual(root.findtext(".//k:Icon/k:href", namespaces=ns),
                             "files/icons/marker.png")
            self.assertEqual(root.findtext(".//k:IconStyle/k:color", namespaces=ns),
                             "ff4837c5")
            self.assertEqual(root.findtext(".//k:IconStyle/k:scale", namespaces=ns),
                             "1.25")
            self.assertEqual(root.findtext(".//k:IconStyle/k:heading", namespaces=ns),
                             "90")
            hot = root.find(".//k:IconStyle/k:hotSpot", ns)
            self.assertEqual(hot.get("x"), "0.5")
            self.assertEqual(hot.get("y"), "0")
            self.assertEqual(root.findtext(".//k:Placemark/k:styleUrl", namespaces=ns),
                             "#new-user-icon")
            self.assertEqual(root.findtext(".//k:ExtendedData/k:Data/k:value",
                                            namespaces=ns),
                             "Map icon created by user")

    def test_custom_center_hotspot_and_invalid_hotspot(self):
        image = minimal_png()
        new_kmz = exporter.kmz_bytes(image, "Centered marker", 31, 30,
                                     anchor_y=0.5)
        with ZipFile(BytesIO(new_kmz)) as archive:
            root = ET.fromstring(archive.read("doc.kml"))
            ns = {"k": "http://www.opengis.net/kml/2.2"}
            self.assertEqual(root.find(".//k:hotSpot", ns).get("y"), "0.5")
        with self.assertRaises(ValueError):
            exporter.kmz_bytes(image, "Bad anchor", 31, 30, anchor_y=1.5)

    def test_invalid_png_rejected(self):
        valid = minimal_png()
        for data in (b"not a png", valid[:-5], valid[:-1],
                     valid[:16] + b"BAD" + valid[19:]):
            with self.subTest(size=len(data)), self.assertRaises(ValueError):
                exporter.kmz_bytes(data, "Place", 31, 30)

    def test_catalog_three_sites_and_distribution_licenses(self):
        catalog = json.loads(
            (ROOT / "references/cartographic-style-sources.json").read_text(
                encoding="utf-8"
            )
        )["sources"]
        by_id = {rec["id"]: rec for rec in catalog}
        self.assertEqual(len(catalog), 21)
        self.assertEqual(len(by_id), 21)
        mapicons = by_id["nicolas-mollet-map-icons"]
        self.assertIn("svg", mapicons["assets"])
        self.assertIn("png", mapicons["assets"])
        self.assertTrue(mapicons["no_hotlinking"])
        streamline = by_id["streamline-google-earth-placemarks"]
        self.assertEqual(streamline["icon_manager_role"],
                         "discovery-only-by-default")
        self.assertIn("DO NOT", streamline["redistribution"])
        self.assertFalse(streamline["recommended_for_new_kmz"])
        mapular = by_id["mapular-map-icon-creator"]
        self.assertEqual(mapular["icon_manager_role"],
                         "design-reference-no-source-code-reuse")
        self.assertIn("NOT", mapular["license"])
        self.assertTrue(mapular["kmz_use"].startswith("new-feature-only"))
        self.assertEqual(by_id["mapbox-maki-icons"]["recommended_for_new_kmz"],
                         True)

    def test_readme_and_specialist_links_and_example(self):
        for name in ("README.md", "README.ar.md", "explorer.html",
                     "skills/gis-cartography-symbology/SKILL.md",
                     "skills/kml-kmz-engineering/SKILL.md"):
            body = (ROOT / name).read_text(encoding="utf-8")
            self.assertIn("unified-gis-icon-manager.md", body, name)
        page = (ROOT / "examples/icon-manager/index.html").read_text(
            encoding="utf-8"
        )
        self.assertIn('id="downloadPNG"', page)
        self.assertIn('id="downloadSVG"', page)
        self.assertIn('document.documentElement.dir=', page)
        self.assertNotIn("<script src=", page)
        self.assertNotIn("https://", page)


if __name__ == "__main__":
    unittest.main()
