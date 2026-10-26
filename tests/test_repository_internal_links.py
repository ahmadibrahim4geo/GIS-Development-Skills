"""Check local Markdown links across all skills, docs and references.

This does not check internet availability or Markdown heading anchors; it catches
missing files, renamed specialists, and dead handoffs created by documentation edits.
"""
import re
import unittest
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
LOCAL_LINK = re.compile(r"\]\(([^)\n]+)\)")


def local_target(source, href):
    address = href.strip().split(" ", 1)[0].strip("<>")
    if not address or address.startswith("#"):
        return None
    if address.startswith(("http://", "https://", "mailto:", "data:", "//")):
        return None
    if "{" in address or "}" in address or "$" in address:
        return None
    parts = urlsplit(address)
    if parts.scheme or not parts.path:
        return None
    candidate = unquote(parts.path)
    if candidate.startswith("/"):
        return ROOT / candidate.lstrip("/")
    return source.parent / candidate


class RepositoryInternalLinksTests(unittest.TestCase):
    def test_linked_local_files_exist(self):
        broken = []
        checked = 0
        for file in sorted(ROOT.rglob("*.md")):
            if any(part in {".git", "node_modules", "vendor"} for part in file.parts):
                continue
            for match in LOCAL_LINK.finditer(file.read_text(encoding="utf-8")):
                target = local_target(file, match.group(1))
                if target is None:
                    continue
                checked += 1
                if not target.exists():
                    broken.append(f"{file.relative_to(ROOT)}: {match.group(1)}")
        self.assertGreater(checked, 120, "Link gate found too few local references")
        self.assertEqual([], broken, "Broken internal links prevent specialist handoffs")


if __name__ == "__main__":
    unittest.main()
