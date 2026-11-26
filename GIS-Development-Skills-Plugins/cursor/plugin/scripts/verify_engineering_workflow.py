#!/usr/bin/env python3
"""Exercise the local engineering workflow on the repository's synthetic DEM."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
TERRAIN = ROOT / "examples/terrain-slope"
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(TERRAIN))

from scripts import engineering_workflow as workflow
from scripts import project_governance as governance
from scripts import test_runs
import slope_ascii


FIXTURE = TERRAIN / "fixtures/planar_slope.asc"
TASK = "P04-FIXTURE"
COMMAND = "terrain.horn-offline"
TEAM_SKILL = "terrain-hydrology-lidar"
ARTIFACT_GROUP = "workflow-slope"


def reviewed_fixture_plan():
    return {
        "schema_version": "1.0", "request_id": "P04-LOCAL-ENGINEERING-FIXTURE", "revision": "r3",
        "original_request": "Verify the local engineering handoffs on the synthetic planar DEM.",
        "language": "en", "status": "draft",
        "approval": {"approved_by_user": False, "approved_revision": None, "high_risk_approved": False},
        "assumptions": [], "open_questions": [],
        "goal": "Verify a real terrain artifact across rework, resume and rollback.",
        "target": "A prepared project test-run workspace with the synthetic planar DEM.",
        "desired_outcomes": ["Nine accepted 45-degree values and a NoData border."],
        "success_criteria": ["Reread the slope grid and match the independent expected bytes."],
        "tasks": [{
            "id": TASK, "title": "Compute and verify planar DEM slope",
            "description": "Run the existing Horn slope action and reopen its output.",
            "priority": "must", "kind": "terrain", "risk": "medium",
            "skills": [TEAM_SKILL, "gis-security-guardian"], "owner_skill": TEAM_SKILL,
            "depends_on": [], "command_id": COMMAND, "trace_id": "P04-PLANAR-DEM",
            "acceptance_criteria": ["The 5 by 5 ASCII grid has nine 45-degree cells and the expected NoData border."],
            "tools": [{"tool_id": COMMAND, "side_effect": effect} for effect in ("read", "write")],
        }],
    }


def expected_hash():
    normal = (ROOT / "fixtures/expected/p04-planar-slope.asc").read_text(encoding="utf-8")
    return hashlib.sha256(normal.replace("\n", os.linesep).encode("utf-8")).hexdigest()


def prepare(project):
    if any(project.iterdir()):
        raise ValueError("Prepare expects a new empty workspace directory")
    governance.init(project)
    shutil.copyfile(FIXTURE, project / "testing data" / FIXTURE.name)
    test_runs.json_write(project / "expected.json", {"checks": [
        {"artifact": f"{ARTIFACT_GROUP}/attempt-03/slope.asc", "comparison": "sha256", "expected": expected_hash()}
    ]})
    return governance.new_test_run(project, "Engineering-Workflow", inputs=(FIXTURE.name,),
                                   expect="expected.json", license_note="MIT synthetic planar DEM")


def dispatch(project, relative_run, stage):
    workspace = governance.safe_path(project, relative_run)
    if workspace.parent != governance.safe_path(project, "testing results"):
        raise ValueError("Select one prepared numbered test run")
    copied = governance.safe_path(workspace, "inputs/" + FIXTURE.name)
    if test_runs.digest(copied) != test_runs.digest(FIXTURE):
        raise ValueError("The controlled example requires its original synthetic fixture")
    plan = reviewed_fixture_plan()
    operation = {"initial": "execute", "repair": "resume", "resume": "resume", "rollback": "rollback"}[stage]

    def authorize(request):
        # The caller explicitly selects one bounded operation on this fixture.
        return (request.workspace == workspace and request.task_id == TASK and request.command_id == COMMAND
                and request.operation == operation and request.plan_sha256 == workflow.digest_json(plan)
                and request.inputs == (FIXTURE.name,) and request.output_group == ARTIFACT_GROUP
                and request.effects == ("read", "write"))

    def execute(inputs, outputs):
        source = inputs[FIXTURE.name]
        header, xkey, ykey, values = slope_ascii.read_grid(source)
        # The first attempt deliberately passes the wrong vertical unit so QA
        # can observe and reject a genuinely different computed raster.
        vertical = "ft" if stage == "initial" else "m"
        slopes = slope_ascii.horn_slope(values, header["nodata_value"], header["cellsize"], "m", vertical)
        slope_ascii.write_result(source, outputs / "slope.asc", header, xkey, ykey, slopes, "m", vertical)

    action = workflow.BoundAction(COMMAND, (FIXTURE.name,), ARTIFACT_GROUP,
                                  ({"artifact": "slope.asc", "comparison": "sha256", "expected": expected_hash()},),
                                  execute)
    controller = workflow.LocalWorkflow(plan, workspace, {TASK: action}, authorize)
    result = controller.rollback(TASK) if stage == "rollback" else controller.run(TASK, resume=operation == "resume")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--run")
    parser.add_argument("stage", choices=("prepare", "initial", "repair", "rollback", "resume"))
    args = parser.parse_args()
    project = args.project.resolve(strict=True)
    if args.stage != "prepare" and not args.run:
        parser.error("Pass the test-run path returned by prepare")
    result = prepare(project) if args.stage == "prepare" else dispatch(project, args.run, args.stage)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
