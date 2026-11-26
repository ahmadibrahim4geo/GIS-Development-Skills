import tempfile
import unittest
from pathlib import Path

from scripts.skill_readiness import inspect


class SkillReadinessTests(unittest.TestCase):
    def setUp(self):
        scratch = tempfile.TemporaryDirectory()
        self.addCleanup(scratch.cleanup)
        self.root = Path(scratch.name).resolve()
        self.suite = self.root / "suite"
        self.suite.mkdir()

    def skill(self, name, parent, files=()):
        directory = parent / name
        directory.mkdir(parents=True)
        (directory / "SKILL.md").write_text(f"---\nname: {name}\ndescription: Local test fixture\n---\n", encoding="utf-8")
        for relative in files:
            path = directory / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("synthetic attachment", encoding="utf-8")
        return directory

    def test_attachment_and_path_presence_do_not_verify_functionality(self):
        directory = self.skill("ui-ux-pro-max", self.suite / "skills", ("scripts/search.py",))
        (directory / "scripts/search.py").write_text("raise RuntimeError('must never execute')", encoding="utf-8")
        result = inspect(self.root, "ui-ux-pro-max", suite=self.suite, which=lambda name: name == "python")
        self.assertEqual(result["status"], "MISSING_REQUIREMENTS")
        self.assertEqual(result["missing_requirements"], ["data/catalog-summary.json"])
        (directory / "data").mkdir()
        (directory / "data/catalog-summary.json").write_text("{}", encoding="utf-8")
        result = inspect(self.root, "ui-ux-pro-max", suite=self.suite, which=lambda name: name == "python")
        self.assertEqual(result["status"], "VERIFY_REQUIRED")
        self.assertEqual(result["functional_test"], "NOT RUN")
        self.assertFalse(result["execution_authorized"])

    def test_provider_has_to_match_the_selected_capability(self):
        folder = self.skill("craft-anything", self.root)
        absent = inspect(self.root, "craft-anything", skill_dir=folder, which=lambda _: None)
        self.assertEqual(absent["status"], "MISSING_REQUIREMENTS")
        self.assertTrue(absent["independent_work_can_continue"])
        result = inspect(self.root, "craft-anything", skill_dir=folder, which=lambda _: None,
                         available_capabilities=["craft-mcp"], require_capabilities=["craft-product-lookup"],
                         source_reviewed=True)
        self.assertEqual(result["missing_requirements"], ["craft-product-lookup"])
        result = inspect(self.root, "craft-anything", skill_dir=folder, which=lambda _: None,
                         available_capabilities=["craft-mcp"], source_reviewed=True)
        self.assertEqual(result["status"], "VERIFY_REQUIRED")

    def test_external_and_quarantine_are_distinct(self):
        installed = self.skill("sample-skill", self.root / ".agents/skills")
        seen = inspect(self.root, "sample-skill", skill_dir=installed)
        self.assertEqual(seen["status"], "SOURCE_REVIEW_REQUIRED")
        candidate = self.skill("sample-skill", self.root / "New Skill")
        isolated = inspect(self.root, "sample-skill", skill_dir=candidate, source_reviewed=True)
        self.assertEqual(isolated["status"], "QUARANTINED")
        with self.assertRaises(ValueError):
            inspect(self.root, "sample-skill", skill_dir=installed, require_files=["../file.txt"])

    def test_github_connector_can_be_considered_without_gh(self):
        (self.suite / "PUBLISHING.md").write_text("# Delivery", encoding="utf-8")
        result = inspect(self.root, "github-delivery", suite=self.suite, which=lambda _: None,
                         available_capabilities=["github-connector"])
        self.assertEqual(result["status"], "VERIFY_REQUIRED")
        self.assertFalse(result["execution_authorized"])
