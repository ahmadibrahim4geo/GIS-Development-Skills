"""Offline regression tests for the local Agent Skills pack validator."""
import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("skill_pack_validation", ROOT / "scripts" / "validate_skill_pack.py")
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class SkillPackValidationTests(unittest.TestCase):
    def test_full_repository(self):
        self.assertEqual([], validator.inspect_repository(ROOT))

    def test_invalid_skill_name_and_long_description(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "skills" / "my-valid-skill" / "SKILL.md"
            path.parent.mkdir(parents=True)
            path.write_text("---\nname: different-name\ndescription: test\n---\n\nHello\n",
                            encoding="utf-8")
            self.assertTrue(any("directory mismatch" in x for x in validator.validate_frontmatter(path)))
            path.write_text("---\nname: my-valid-skill\ndescription: " + "x" * 1025
                            + "\n---\n\nHello\n", encoding="utf-8")
            self.assertTrue(any("1024" in x for x in validator.validate_frontmatter(path)))

    def test_missing_link_is_detected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            md = root / "README.md"
            md.write_text("[Missing](references/absent.md)", encoding="utf-8")
            self.assertTrue(any("missing local target" in x for x in
                                validator.check_links(md, root)))

    def test_outside_root_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            md = root / "README.md"
            md.write_text("[Bad](../outside.md)", encoding="utf-8")
            self.assertTrue(any("escapes repository" in x for x in
                                validator.check_links(md, root)))

    def test_skill_counter_must_match_actual_skills(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skill = root / "skills" / "demo" / "SKILL.md"
            skill.parent.mkdir(parents=True)
            skill.write_text("---\nname: demo\ndescription: A GIS demo.\n---\n\nHello\n", encoding="utf-8")
            index = root / "explorer.html"
            index.write_text('<div class="stat"><strong>09</strong><span data-i18n="statSkill">Skills</span></div>',
                             encoding="utf-8")
            self.assertTrue(any("skill counter" in x for x in validator.inspect_repository(root)))
            index.write_text('<div class="stat"><strong>01</strong><span data-i18n="statSkill">Skills</span></div>',
                             encoding="utf-8")
            self.assertEqual([], validator.inspect_repository(root))


if __name__ == "__main__":
    unittest.main()
