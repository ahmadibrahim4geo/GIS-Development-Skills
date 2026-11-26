"""Regression guard against duplicate push + pull_request workflow fanout."""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class WorkflowEventPolicyTests(unittest.TestCase):
    def test_validate_and_security_scoped_concurrent_events(self):
        for name in ("validate", "security"):
            with self.subTest(name=name):
                content = (ROOT / ".github" / "workflows" /
                           (name + ".yml")).read_text(encoding="utf-8")
                self.assertIn("push:\n    branches:\n      - main", content)
                self.assertIn("  pull_request:\n", content)
                self.assertIn("  workflow_dispatch:\n", content)
                self.assertIn("concurrency:\n", content)
                self.assertIn("cancel-in-progress: true", content)
                self.assertIn("github.event.pull_request.number || github.ref", content)
                self.assertIn("contents: read", content)
                self.assertIn("python scripts/", content)

    def test_documented_failure_diagnosis(self):
        guide = (ROOT / "docs/GITHUB_ACTIONS_TROUBLESHOOTING.md").read_text(encoding="utf-8")
        for term in ("Run offline unit tests", "Validate skill pack", "Security Guardian",
                     "latest run", "FAIL:"):
            self.assertIn(term, guide)


if __name__ == "__main__":
    unittest.main()
