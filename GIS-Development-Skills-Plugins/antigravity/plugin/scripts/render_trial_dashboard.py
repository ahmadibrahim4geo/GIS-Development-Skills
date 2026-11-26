#!/usr/bin/env python3
"""Render a local trial overview from phase state and observed test receipts."""
import argparse
from html import escape
import json
from pathlib import Path


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def render(state, evidence, release):
    revision = escape(str(evidence["revision"]))
    if release["revision"] != evidence["revision"] or state["request_id"] != evidence["request_id"]:
        raise ValueError("Trial, phase state and evidence must refer to the same request and revision.")
    archive = str(release["archive"])
    if archive != "gis-development-suite.zip":
        raise ValueError("Expected a local trial archive beside the dashboard.")
    rows = "".join(
        f'<tr><th scope="row"><bdi>{escape(phase)}</bdi></th><td><bdi>{escape(status)}</bdi></td></tr>'
        for phase, status in state["phases"].items()
    )
    checks = "".join(
        f'<tr><th scope="row">{escape(row["label_ar"])} <bdi lang="en">{escape(row["label_en"])}</bdi></th>'
        f'<td><bdi>{escape(row["status"])}</bdi></td><td><bdi>{escape(row["tier"])}</bdi></td></tr>'
        for row in evidence["scenarios"]
    )
    digest = escape(release["archive_sha256"])
    base_commit = escape(release["base_commit"])
    return f"""<!doctype html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>GIS Development Skills · حالة النسخة التجريبية</title>
<style>
:root {{ color-scheme: dark; background: #101b1e; color: #e4f2ed; font: 16px system-ui, sans-serif; }}
main {{ width: min(64rem, calc(100% - 2rem)); margin: 3rem auto; }}
h1 {{ font-size: clamp(1.5rem, 5vw, 2.8rem); margin-block-end: .3rem; }}
h2 {{ margin-block-start: 2rem; }}
table {{ width: 100%; border-collapse: collapse; text-align: start; }}
th, td {{ text-align: start; padding: .6rem; border-block-end: 1px solid #354a49; }}
a, h2 {{ color: #95ecd3; }}
a:focus-visible {{ outline: 2px solid #95ecd3; outline-offset: 4px; }}
code {{ overflow-wrap: anywhere; }}
bdi[lang="en"] {{ display: block; color: #b4cdc4; font-weight: 400; }}
</style>
</head>
<body>
<main>
<h1 lang="en" dir="ltr">GIS Development Skills</h1>
<p lang="en" dir="ltr">The Heart of Geospatial Innovation</p>
<h2>النسخة التجريبية المحلية <bdi lang="en">Local user-testing build · {revision}</bdi></h2>
<p><a href="{archive}">تحميل الحزمة التجريبية <bdi lang="en">Download trial ZIP</bdi></a></p>
<p>بصمة الحزمة <bdi><code>{digest}</code></bdi></p>
<p>الـcommit الأساسي <bdi><code>{base_commit}</code></bdi></p>
<h2>قبول التشغيل <bdi lang="en">Scenario acceptance</bdi></h2>
<table><thead><tr><th scope="col">السيناريو</th><th scope="col">الحالة</th><th scope="col">مستوى الدليل</th></tr></thead>
<tbody>{checks}</tbody></table>
<h2>المراحل <bdi lang="en">Development phases</bdi></h2>
<table><thead><tr><th scope="col">المرحلة</th><th scope="col">الحالة</th></tr></thead>
<tbody>{rows}</tbody></table>
</main>
</body>
</html>
"""


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--status", type=Path, required=True)
    parser.add_argument("--evidence", type=Path, required=True)
    parser.add_argument("--release", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    html = render(load(args.status), load(args.evidence), load(args.release))
    with args.output.open("x", encoding="utf-8") as handle:
        handle.write(html)


if __name__ == "__main__":
    main()
