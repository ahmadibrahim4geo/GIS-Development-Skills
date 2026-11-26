#!/usr/bin/env python3
"""Render the QGIS point export in a local Chromium process and verify DOM readback."""
import argparse
from html.parser import HTMLParser
import hashlib
import json
from pathlib import Path
import subprocess


class Readback(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reading = False
        self.text = ""

    def handle_starttag(self, tag, attrs):
        if tag == "output" and dict(attrs).get("id") == "result":
            self.reading = True

    def handle_data(self, data):
        if self.reading:
            self.text += data

    def handle_endtag(self, tag):
        if tag == "output":
            self.reading = False


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--browser", type=Path, required=True)
    parser.add_argument("--geojson", type=Path, required=True)
    parser.add_argument("--work", type=Path, required=True)
    args = parser.parse_args()
    browser = args.browser.resolve(strict=True)
    work = args.work.absolute()
    work.mkdir()
    with args.geojson.open("rb") as handle:
        raw = handle.read(65537)
    if len(raw) > 65536:
        raise ValueError("Point fixture exceeds 64 KiB")
    fixture = json.dumps(json.loads(raw), ensure_ascii=True).replace("<", "\\u003c")
    template = Path(__file__).with_name("web-geojson-readback.html").read_text(encoding="utf-8")
    fixture_page = work / "geojson-readback.html"
    fixture_page.write_text(template.replace("__FIXTURE__", fixture, 1), encoding="utf-8")
    result = subprocess.run(
        [str(browser), "--headless", "--no-first-run", "--disable-background-networking",
         "--disable-default-apps", f"--user-data-dir={work / 'profile'}", "--dump-dom",
         fixture_page.as_uri()], cwd=work, stdin=subprocess.DEVNULL, capture_output=True,
        text=True, encoding="utf-8", errors="replace", timeout=35,
    )
    (work / "browser.log").write_text(result.stderr, encoding="utf-8")
    if result.returncode:
        raise RuntimeError(f"Browser exited {result.returncode}. See browser.log.")
    (work / "dom.html").write_text(result.stdout, encoding="utf-8")
    parsed = Readback()
    parsed.feed(result.stdout)
    observed = json.loads(parsed.text)
    actual = {point["name"]: (point["x"], point["y"]) for point in observed["points"]}
    expected = {"Cairo": (179, 108), "Alexandria": (73, 44)}
    if (len(observed["points"]) != len(expected) or actual != expected
            or not all(observed[name] is True for name in ("keyboardFocus", "hidden", "restored"))):
        raise RuntimeError(f"Browser point placement or toggle failed: {observed}")
    receipt = {"status": "PASS", "browser": browser.name, "source_sha256": hashlib.sha256(raw).hexdigest(),
               "crs": "EPSG:4326", "browser_readback": observed}
    encoded = json.dumps(receipt, indent=2)
    (work / "WEB_ACCEPTANCE.json").write_text(encoded + "\n", encoding="utf-8")
    print(encoded)


if __name__ == "__main__":
    main()
