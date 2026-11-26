"""Root unittest adapter exposing plugin-system/tests/test_p09_platform_adapters.py."""

import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "plugin-system" / "tests" / "test_p09_platform_adapters.py"


def load_tests(loader, tests, pattern):
    spec = importlib.util.spec_from_file_location("plugin_system_test_p09", TARGET)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["plugin_system_test_p09"] = mod
    spec.loader.exec_module(mod)
    return loader.loadTestsFromModule(mod)
