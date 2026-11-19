"""Task-local verification receipts; no native GIS execution or publishing."""
import concurrent.futures
import json
import os
import platform
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
COMMANDS = {
    "catalog": ["scripts/validate_catalog.py"],
    "api-catalog": ["scripts/validate_api_catalog.py"],
    "skill-pack": ["scripts/validate_skill_pack.py"],
    "manifest": ["scripts/build_manifest.py", "--check"],
    "skill-flow": ["scripts/audit_skill_graph.py"],
    "security": ["scripts/security_audit.py", "--root", ".", "--format", "text"],
    "architecture-flow": ["scripts/validate_architecture_flow.py", "examples/architecture-visualization/qgis-ribbon.flow.json"],
    "architecture-plan": ["scripts/intent_router.py", "--plan", "examples/architecture-visualization/qgis-ribbon.plan.json", "--workflow", "--format", "json"],
    "unit-tests": ["-m", "unittest", "discover", "-s", "tests", "-v"],
    "diff-check": ["git", "diff", "--check"],
}


def run(item):
    name, args = item
    command = args if name == "diff-check" else [sys.executable, "-X", "utf8", "-B", *args]
    env = {**os.environ, "PYTHONUTF8": "1", "PYTHONDONTWRITEBYTECODE": "1"}
    start = time.monotonic()
    result = subprocess.run(command, cwd=ROOT, env=env, capture_output=True, text=True, encoding="utf-8", errors="replace")
    (OUT / (name + ".log")).write_text(result.stdout + result.stderr, encoding="utf-8")
    return {"name": name, "command": command, "returncode": result.returncode,
            "status": "PASS" if result.returncode == 0 else "FAIL", "seconds": round(time.monotonic() - start, 3),
            "log": str((OUT / (name + ".log")).relative_to(ROOT))}


if __name__ == "__main__":
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(run, COMMANDS.items()))
    receipt = {"request_id": "ARCH-INTENT-001", "revision": "r1", "python": sys.version,
               "os": platform.platform(), "native_gis_execution": "NOT RUN", "archify_render": "NOT RUN",
               "checks": results}
    (OUT / "checks.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for result in results:
        print(result["name"], result["status"], result["log"])
    sys.exit(0 if all(result["returncode"] == 0 for result in results) else 1)
