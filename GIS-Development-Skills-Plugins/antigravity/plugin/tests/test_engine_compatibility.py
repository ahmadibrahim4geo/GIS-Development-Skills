#!/usr/bin/env python3
"""Tests for scripts/inventory_ui_actions.py and Qt .ui integration in gis_ui_command_audit.py (E25, E26, E-26)."""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts import gis_ui_command_audit, inventory_ui_actions  # noqa: E402


SAMPLE_QT_UI = """<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>QgisApp</class>
 <widget class="QMainWindow" name="QgisApp">
  <widget class="QMenuBar" name="menubar">
   <widget class="QMenu" name="mProjectMenu">
    <addaction name="mActionSaveProject"/>
   </widget>
  </widget>
  <widget class="QToolBar" name="mFileToolBar">
   <addaction name="mActionSaveProject"/>
   <addaction name="mActionZoomIn"/>
  </widget>
  <action name="mActionSaveProject">
   <property name="text"><string>&amp;Save</string></property>
   <property name="toolTip"><string>Save Project</string></property>
   <property name="shortcut"><string>Ctrl+S</string></property>
  </action>
  <action name="mActionZoomIn">
   <property name="text"><string>Zoom In</string></property>
   <property name="checkable"><bool>true</bool></property>
  </action>
 </widget>
</ui>
"""


class EngineCompatibilityQtUITests(unittest.TestCase):
    """Verifies bounded Qt .ui inventory extraction and negative security guards."""

    def test_qt_ui_action_and_placement_extraction_and_audit_integration(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ui_file = root / "qgisapp.ui"
            ui_file.write_text(SAMPLE_QT_UI, encoding="utf-8")

            report = inventory_ui_actions.inventory_tree(root)
            self.assertEqual(report["files_scanned"], 1)
            self.assertEqual(report["action_count"], 2)
            self.assertFalse(report["handlers_verified"])
            self.assertFalse(report["dynamic_actions_verified"])
            self.assertEqual(report["errors"], [])

            actions = {a["action_id"]: a for a in report["files"][0]["actions"]}
            self.assertEqual(actions["mActionSaveProject"]["shortcut"], "Ctrl+S")
            self.assertEqual(len(actions["mActionSaveProject"]["placements"]), 2)
            self.assertTrue(actions["mActionZoomIn"]["checkable"])
            self.assertEqual(actions["mActionZoomIn"]["handler_state"], "unresolved")

            # Verify integrated gis_ui_command_audit.py delegation.
            integrated = gis_ui_command_audit.audit_tree(root, include_qt_ui=True)
            self.assertIn("qt_ui_inventory", integrated)
            self.assertEqual(integrated["qt_ui_inventory"]["action_count"], 2)

            cli = subprocess.run(
                [sys.executable, str(ROOT / "scripts" / "inventory_ui_actions.py"), "--root", str(root), "--format", "json"],
                capture_output=True,
                text=True,
                timeout=20,
            )
            self.assertEqual(cli.returncode, 0, cli.stderr)
            self.assertEqual(json.loads(cli.stdout)["action_count"], 2)

    def test_qt_ui_security_limits_block_dtd_oversize_and_traversal(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            dtd_file = root / "evil_dtd.ui"
            dtd_file.write_text('<!DOCTYPE foo [<!ENTITY xxe "bad">]><ui version="4.0"></ui>', encoding="utf-8")
            with self.assertRaises(ValueError):
                inventory_ui_actions.inspect_qt_ui(dtd_file, root=root)

            huge_file = root / "oversize.ui"
            huge_file.write_text("<ui>" + ("x" * (inventory_ui_actions.MAX_UI_FILE_BYTES + 32)) + "</ui>", encoding="utf-8")
            with self.assertRaises(ValueError):
                inventory_ui_actions.inspect_qt_ui(huge_file, root=root)

            outside_dir = root.parent / "outside.ui"
            with self.assertRaises(ValueError):
                inventory_ui_actions.inspect_qt_ui(outside_dir, root=root)


if __name__ == "__main__":
    unittest.main()
