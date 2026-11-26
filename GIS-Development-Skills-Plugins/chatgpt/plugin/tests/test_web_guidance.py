"""Offline checks for the paired frontend provider boundary."""

import io
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from scripts import web_guidance


class WebGuidanceTests(unittest.TestCase):
    def test_tampered_package_and_missing_ui_prevent_provider_execution(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            archive = root / web_guidance.ARCHIVE_NAME
            archive.write_bytes(b"unexpected artifact")
            with patch.object(web_guidance, "run") as run:
                with self.assertRaisesRegex(web_guidance.GuidanceError, r"does not match[\s\S]*UI/UX Pro Max"):
                    web_guidance.prerequisites(root, archive, root / "absent")
            run.assert_not_called()

    def test_preflight_checks_the_actual_node_version(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            archive = root / web_guidance.ARCHIVE_NAME
            archive.touch()
            for relative in web_guidance.UI_FILES:
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("fixture", encoding="utf-8")
            with patch.object(web_guidance, "verified_archive", return_value=b"verified"), \
                    patch.object(web_guidance.shutil, "which", return_value="node"), \
                    patch.object(web_guidance, "run", return_value="v20.0.0"):
                with self.assertRaisesRegex(web_guidance.GuidanceError, r"Node.js 22"):
                    web_guidance.prerequisites(root, archive, root)

    def test_run_disables_telemetry_and_preserves_long_output(self):
        guide = "# Guide\n" + ("example\n" * 2000)

        def run_child(command, **kwargs):
            self.assertEqual(command, ["node", "entry", "retrieve", "dialog"])
            self.assertEqual(kwargs["env"]["DISABLE_TELEMETRY"], "1")
            self.assertEqual(kwargs["env"]["ENABLE_FILE_LOGGING"], "false")
            self.assertNotIn("NODE_OPTIONS", kwargs["env"])
            kwargs["stdout"].write(guide.encode("utf-8"))
            return subprocess.CompletedProcess(command, 0, stderr=b"")

        with patch.object(web_guidance.tempfile, "TemporaryFile", side_effect=io.BytesIO), \
                patch.object(web_guidance.subprocess, "run", side_effect=run_child):
            self.assertEqual(web_guidance.run(["node", "entry", "retrieve", "dialog"], Path.cwd()), guide)
