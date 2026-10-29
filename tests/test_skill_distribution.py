import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "build_skill_bundle.py"
SPEC = importlib.util.spec_from_file_location("build_skill_bundle", SCRIPT)
bundle = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(bundle)


class SkillDistributionTests(unittest.TestCase):
    def test_build_is_self_contained_and_deterministic(self):
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            base = Path(temporary)
            first = bundle.build(base / "one")
            second = bundle.build(base / "two")

            self.assertEqual("PASS", first["status"])
            self.assertEqual(first["archive_sha256"], second["archive_sha256"])
            self.assertEqual(
                hashlib.sha256(Path(first["archive"]).read_bytes()).hexdigest(),
                first["archive_sha256"],
            )

            expanded = Path(first["bundle_directory"])
            self.assertFalse((expanded / ".git").exists())
            self.assertFalse((expanded / ".agent-development-log").exists())
            self.assertTrue((expanded / "skills" / "gis-development" / "SKILL.md").is_file())
            self.assertTrue((expanded / "references" / "repository-manifest.json").is_file())
            self.assertTrue((expanded / "scripts" / "intent_router.py").is_file())

            manifest = json.loads((expanded / "bundle-manifest.json").read_text("utf-8"))
            expected_skills = len(list((ROOT / "skills").glob("*/SKILL.md")))
            self.assertEqual(expected_skills, manifest["inventory"]["skill_count"])
            self.assertEqual(manifest["file_count"], len(manifest["files"]))
            self.assertEqual([], first["audit"]["broken_local_markdown_links"])
            self.assertEqual("NOT_RUN", first["audit"]["native_gis_execution"])
            self.assertEqual("NOT_RUN", first["audit"]["agent_client_installation"])

            archive_audit = bundle.audit_path(Path(first["archive"]))
            self.assertEqual("PASS", archive_audit["status"])

    def test_refuses_to_overwrite_bundle_outputs(self):
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            output = Path(temporary) / "release"
            bundle.build(output)
            with self.assertRaises(bundle.BundleError):
                bundle.build(output)

    def test_audit_detects_tampering(self):
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            result = bundle.build(Path(temporary) / "release")
            expanded = Path(result["bundle_directory"])
            target = expanded / "skills" / "gis-development" / "SKILL.md"
            target.write_text(target.read_text("utf-8") + "\nchanged\n", encoding="utf-8")
            with self.assertRaises(bundle.BundleError):
                bundle.audit_directory(expanded)

    def test_sensitive_names_are_blocked(self):
        self.assertTrue(bundle.is_sensitive(Path("skills/demo/.env")))
        self.assertTrue(bundle.is_sensitive(Path("skills/demo/private.pem")))
        self.assertFalse(bundle.is_sensitive(Path("skills/demo/SKILL.md")))


if __name__ == "__main__":
    unittest.main()
