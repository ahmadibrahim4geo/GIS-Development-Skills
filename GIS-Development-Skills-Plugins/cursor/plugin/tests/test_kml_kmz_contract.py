"""Offline KML/KMZ safety and geometry contract tests (stdlib only)."""
import io
import unittest
import zipfile
import xml.etree.ElementTree as ET
from pathlib import PurePosixPath

MAX_MEMBERS = 100
MAX_TOTAL_BYTES = 5_000_000
MAX_MEMBER_BYTES = 2_000_000
MAX_RATIO = 100


def validate_kmz(blob):
    """Preflight archive entries before any extraction or XML parsing."""
    with zipfile.ZipFile(io.BytesIO(blob)) as archive:
        members = archive.infolist()
        if len(members) > MAX_MEMBERS:
            raise ValueError("too many members")
        total = 0
        names = set()
        for info in members:
            name = info.filename.replace("\\", "/")
            path = PurePosixPath(name)
            if (not name or name.startswith("/") or name.startswith("//")
                    or ":" in path.parts[0] or ".." in path.parts
                    or "\x00" in name):
                raise ValueError("unsafe path")
            if name in names:
                raise ValueError("duplicate entry")
            names.add(name)
            if info.flag_bits & 1:
                raise ValueError("encrypted member")
            if ((info.external_attr >> 16) & 0o170000) == 0o120000:
                raise ValueError("symlink")
            if info.file_size > MAX_MEMBER_BYTES:
                raise ValueError("oversized member")
            total += info.file_size
            if total > MAX_TOTAL_BYTES:
                raise ValueError("oversized archive")
            if info.file_size and info.file_size / max(1, info.compress_size) > MAX_RATIO:
                raise ValueError("suspicious compression ratio")
        if not any(name.lower().endswith(".kml") for name in names):
            raise ValueError("missing KML")
    return True


def make_zip(entries):
    data = io.BytesIO()
    with zipfile.ZipFile(data, "w", zipfile.ZIP_DEFLATED) as z:
        for name, value in entries:
            z.writestr(name, value)
    return data.getvalue()


class TestKmlKmz(unittest.TestCase):
    def test_basic_kml_coordinates(self):
        root = ET.fromstring('<kml xmlns="http://www.opengis.net/kml/2.2"><Placemark><Point><coordinates>31.2,30.1,5</coordinates></Point></Placemark></kml>')
        ns = {"k": "http://www.opengis.net/kml/2.2"}
        coords = root.find(".//k:coordinates", ns).text.split(",")
        self.assertEqual(coords, ["31.2", "30.1", "5"])

    def test_valid_kmz(self):
        self.assertTrue(validate_kmz(make_zip([("doc.kml", "<kml/>"), ("icons/p.png", b"png")])))

    def test_traversal_rejected(self):
        with self.assertRaises(ValueError):
            validate_kmz(make_zip([("../escape.kml", "x")]))

    def test_absolute_rejected(self):
        with self.assertRaises(ValueError):
            validate_kmz(make_zip([("/tmp/doc.kml", "x")]))

    def test_windows_drive_rejected(self):
        with self.assertRaises(ValueError):
            validate_kmz(make_zip([("C:/doc.kml", "x")]))

    def test_missing_kml_rejected(self):
        with self.assertRaises(ValueError):
            validate_kmz(make_zip([("icon.png", "x")]))

    def test_duplicate_rejected(self):
        import warnings
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            data = make_zip([("doc.kml", "x"), ("doc.kml", "y")])
        with self.assertRaises(ValueError):
            validate_kmz(data)

    def test_large_member_rejected(self):
        with self.assertRaises(ValueError):
            validate_kmz(make_zip([("doc.kml", b"x" * (MAX_MEMBER_BYTES + 1))]))


if __name__ == "__main__":
    unittest.main()
