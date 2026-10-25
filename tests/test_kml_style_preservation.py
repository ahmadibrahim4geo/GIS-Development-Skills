"""Offline regression for imported KMZ styling: style nodes + resource integrity."""
from io import BytesIO
import importlib.util
import json
from pathlib import Path
import unittest
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "examples/kml-style-preservation/verify_kmz_style.py"
spec = importlib.util.spec_from_file_location("verify_kmz_style", MODULE)
kmz = importlib.util.module_from_spec(spec)
spec.loader.exec_module(kmz)

KML = """<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
<Document>
 <Style id="normal">
  <IconStyle><color>ff22aa44</color><scale>1.3</scale><heading>17</heading>
   <Icon><href>files/pin.png</href></Icon>
   <hotSpot x="0.5" y="0" xunits="fraction" yunits="fraction"/>
  </IconStyle><LabelStyle><color>ff0033ee</color><scale>1.2</scale></LabelStyle>
 </Style>
 <Style id="highlight"><IconStyle><scale>1.8</scale>
  <Icon><href>files/pin.png</href></Icon></IconStyle></Style>
 <StyleMap id="choose">
  <Pair><key>normal</key><styleUrl>#normal</styleUrl></Pair>
  <Pair><key>highlight</key><styleUrl>#highlight</styleUrl></Pair>
 </StyleMap>
 <Folder><name>Original author folder</name>
  <Placemark><name>Site</name><styleUrl>#choose</styleUrl>
   <Point><coordinates>31,30,0</coordinates></Point></Placemark>
  <Placemark><name>River</name><Style><LineStyle><color>ffff0000</color>
   <width>4.2</width></LineStyle></Style>
   <LineString><coordinates>31,30 31.2,30.2</coordinates></LineString></Placemark>
  <Placemark><name>Area</name><Style><PolyStyle><color>7f00ff00</color>
   <fill>1</fill><outline>0</outline></PolyStyle></Style>
   <Polygon><outerBoundaryIs><LinearRing><coordinates>31,30 32,30 32,31 31,30</coordinates>
   </LinearRing></outerBoundaryIs></Polygon></Placemark>
 </Folder>
</Document></kml>"""


def make_kmz(xml=KML, icon=b"our-own-synthetic-icon", extra=None):
    buffer = BytesIO()
    with ZipFile(buffer, "w", compression=ZIP_DEFLATED) as archive:
        archive.writestr("doc.kml", xml)
        archive.writestr("files/pin.png", icon)
        if extra:
            for name, body in extra.items():
                archive.writestr(name, body)
    return BytesIO(buffer.getvalue())


class KMZPreservationTests(unittest.TestCase):
    def test_same_style_repacked_is_accepted(self):
        got = kmz.compare_archives(make_kmz(), make_kmz(xml=KML.replace(" <Style id=", "\n  <Style id=")))
        self.assertTrue(got["style_equal"])
        self.assertTrue(got["asset_equal"])

    def test_recoloring_a_line_is_detected(self):
        got = kmz.compare_archives(make_kmz(), make_kmz(xml=KML.replace("ffff0000", "ff0000ff")))
        self.assertFalse(got["style_equal"])
        self.assertTrue(got["asset_equal"])

    def test_icon_bytes_change_is_detected(self):
        got = kmz.compare_archives(make_kmz(), make_kmz(icon=b"new-default-icon"))
        self.assertTrue(got["style_equal"])
        self.assertFalse(got["asset_equal"])

    def test_stylemap_reference_change_is_detected(self):
        revised = KML.replace('<styleUrl>#highlight</styleUrl>', '<styleUrl>#normal</styleUrl>')
        self.assertFalse(kmz.compare_archives(make_kmz(), make_kmz(xml=revised))["style_equal"])

    def test_missing_icon_is_detected(self):
        with ZipFile(make_kmz(), "r") as old:
            buf = BytesIO()
            with ZipFile(buf, "w", compression=ZIP_DEFLATED) as out:
                out.writestr("doc.kml", old.read("doc.kml"))
        self.assertFalse(kmz.compare_archives(make_kmz(), BytesIO(buf.getvalue()))["asset_equal"])

    def test_zip_member_path_traversal_rejected(self):
        with self.assertRaises(ValueError):
            kmz.inspect_kmz(make_kmz(extra={"../unsafe.png": b"x"}))

    def test_external_entity_blocked(self):
        evil = "<!DOCTYPE kml [<!ENTITY x SYSTEM 'file:///etc/passwd'>]>" + KML
        with self.assertRaises(ValueError):
            kmz.inspect_kmz(make_kmz(xml=evil))

    def test_catalog_icon_licenses_and_roles(self):
        records = json.loads((ROOT/"references/cartographic-style-sources.json").read_text(encoding="utf-8"))["sources"]
        ids = {item["id"] for item in records}
        self.assertGreaterEqual(len(records), 19)
        for required in ("pinhead-map-icons", "mapbox-maki-icons", "temaki-map-icons",
                         "nicolas-mollet-map-icons", "scott-map-icons", "leaflet-extra-markers",
                         "google-material-symbols", "leaflet-awesome-markers", "cesium-pinbuilder"):
            self.assertIn(required, ids)
        for item in records:
            if item["id"] in {"pinhead-map-icons", "mapbox-maki-icons", "temaki-map-icons",
                             "nicolas-mollet-map-icons", "scott-map-icons", "leaflet-extra-markers",
                             "google-material-symbols", "leaflet-awesome-markers", "cesium-pinbuilder"}:
                self.assertIn("new-feature-only", item["kmz_use"] if item["id"] != "cesium-pinbuilder"
                              else "new-feature-only: " + item["kmz_use"])
                self.assertTrue(item["license_evidence_url"].startswith("https://"))


if __name__ == "__main__":
    unittest.main()
