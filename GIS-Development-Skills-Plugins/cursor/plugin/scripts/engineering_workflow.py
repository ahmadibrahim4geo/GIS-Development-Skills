"""Local engineering handoffs with host-bound actions and persisted evidence."""

from copy import deepcopy
from dataclasses import dataclass, replace
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import tempfile
from typing import Callable

if __package__:
    from . import intent_router, test_runs, verify_completion
    from .project_structure import safe_path
else:
    import intent_router
    import test_runs
    import verify_completion
    from project_structure import safe_path


ROOT = Path(__file__).resolve().parents[1]
ROLE_REGISTRY = ROOT / "references/engineering-role-registry.json"
MODE = "SEQUENTIAL_ROLE_SIMULATION"
MAX_ATTEMPTS = 12
RISK_PROFILE = {"low": "LITE", "medium": "STANDARD", "high": "DEEP", "critical": "DEEP"}
CONDITIONAL_ROLES = {"structure", "research", "toolchain", "designer", "gis", "remote-sensing", "rendering"}
RENDERING_KINDS = {"3d", "rendering", "terrain-rendering", "desktop-globe", "terrain-viewport"}


@dataclass(frozen=True)
class BoundAction:
    command_id: str
    inputs: tuple[str, ...]
    output_group: str
    checks: tuple[dict, ...]
    execute: Callable[[dict[str, Path], Path], None]


@dataclass(frozen=True)
class AuthorizationRequest:
    request_id: str
    revision: str
    plan_sha256: str
    task_id: str
    command_id: str
    workspace: Path
    operation: str
    effects: tuple[str, ...]
    inputs: tuple[str, ...]
    output_group: str


def digest_json(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, allow_nan=False).encode("utf-8")).hexdigest()


def role_plan(task, registry=None):
    registry = verify_completion.read_json(ROLE_REGISTRY) if registry is None else registry
    roles = {role["id"]: role for role in registry["roles"]}
    known = intent_router.available_skills()
    if (registry.get("schema_version") != "1.0" or len(roles) != len(registry["roles"])
            or any(not set(role["skills"]) <= known for role in roles.values())):
        raise ValueError("Invalid role registry or unknown skill")
    profile = RISK_PROFILE[task["risk"]]
    selected = registry["profiles"][profile]
    if len(selected) != len(set(selected)) or not set(selected) <= roles.keys():
        raise ValueError("Invalid role assignments for the selected profile")
    ids = set(selected)
    for role_id in CONDITIONAL_ROLES:
        if role_id == "rendering" and task["kind"].casefold() not in RENDERING_KINDS:
            continue
        if set(task["skills"]) & set(roles[role_id]["skills"]):
            ids.add(role_id)
    return {"profile": profile, "roles": [role for role_id, role in roles.items() if role_id in ids]}


class LocalWorkflow:
    """The host supplies trusted callables and an authorizer for each invocation."""

    def __init__(self, plan, workspace, actions, authorize):
        plan = deepcopy(plan)
        compiled = intent_router.compile_workflow(plan)
        if not compiled["valid"]:
            raise ValueError("Invalid reviewed workflow: " + "; ".join(compiled["errors"]))
        self.tasks = {task["id"]: task for task in plan["tasks"]}
        self.request_id, self.revision = plan["request_id"], plan["revision"]
        self.plan_sha = digest_json(plan)
        self.workspace = Path(workspace).resolve(strict=True)
        self.manifest = verify_completion.read_json(safe_path(self.workspace, "RUN.json"),
                                                    max_bytes=test_runs.MAX_RECEIPT)
        self.inputs = {entry["path"]: entry for entry in self.manifest["inputs"]}
        self.actions = {key: replace(action, checks=deepcopy(action.checks))
                        for key, action in actions.items()}
        self.authorize = authorize
        if self.tasks.keys() != self.actions.keys():
            raise ValueError("Trusted host bindings must cover exactly the reviewed tasks")
        registry = verify_completion.read_json(ROLE_REGISTRY)
        self.teams = {task_id: role_plan(task, registry) for task_id, task in self.tasks.items()}
        self.groups = {}
        contract = {}
        for task_id, binding in self.actions.items():
            task = self.tasks[task_id]
            effects = {tool["side_effect"] for tool in task.get("tools", [])}
            if not {"read", "write"} <= effects or effects - {"read", "write"}:
                raise ValueError("Local fixture execution requires the declared read/write effects only")
            if not binding.command_id or task.get("command_id", binding.command_id) != binding.command_id:
                raise ValueError("Trusted binding does not match the reviewed command ID")
            if not binding.inputs or not set(binding.inputs) <= self.inputs.keys():
                raise ValueError("Binding inputs must be identified in the prepared run")
            if len(binding.checks) != len(task["acceptance_criteria"]):
                raise ValueError("Each reviewed acceptance criterion needs an independent readback")
            group = safe_path(self.workspace, "outputs/" + binding.output_group)
            if group == safe_path(self.workspace, "outputs") or any(
                    group.is_relative_to(other) or other.is_relative_to(group)
                    for other in self.groups.values()):
                raise ValueError("The output group overlaps another task or the output root")
            self.groups[task_id] = group
            for check in binding.checks:
                if set(check) != {"artifact", "comparison", "expected"} or check["comparison"] not in ("json", "sha256"):
                    raise ValueError("Invalid trusted output check")
                predicted = safe_path(group, check["artifact"])
                if predicted.parent == group and predicted.name.casefold() in {"readback.json", "doneproof.json"}:
                    raise ValueError("Output check points to a reserved receipt name")
            contract[task_id] = {"command_id": binding.command_id, "inputs": binding.inputs,
                                 "output_group": binding.output_group, "checks": binding.checks}
        self.contract_sha = digest_json({"actions": contract, "manifest": self.manifest})

    def _grant(self, task_id, operation):
        action = self.actions[task_id]
        request = AuthorizationRequest(self.request_id, self.revision, self.plan_sha, task_id,
                                       action.command_id, self.workspace, operation,
                                       ("read", "write"), action.inputs, action.output_group)
        if self.authorize(request) is not True:
            raise PermissionError("Trusted host did not grant the requested local operation")

    def _load(self):
        path = safe_path(self.workspace, "WORKFLOW.json")
        if not path.exists():
            return {"schema_version": "1.0", "request_id": self.request_id, "revision": self.revision,
                    "plan_sha256": self.plan_sha, "contract_sha256": self.contract_sha, "host_mode": MODE,
                    "tasks": {key: {"state": "PLANNED", "attempts": 0, "events": []} for key in self.tasks}}
        data = verify_completion.read_json(path, max_bytes=test_runs.MAX_RECEIPT)
        if data.get("plan_sha256") != self.plan_sha or data.get("contract_sha256") != self.contract_sha:
            raise ValueError("Review and start a new run for a changed plan or binding contract")
        return data

    def _store(self, data):
        path = safe_path(self.workspace, "WORKFLOW.json")
        with tempfile.TemporaryDirectory(prefix=".checkpoint-", dir=self.workspace) as directory:
            temporary = Path(directory) / "WORKFLOW.json"
            test_runs.json_write(temporary, data)
            os.replace(temporary, path)

    def _event(self, data, task_id, state, role, **details):
        row = data["tasks"][task_id]
        row["state"] = state
        row["events"].append({"state": state, "role": role, "attempt": row["attempts"],
                              "at": datetime.now(timezone.utc).isoformat(), **details})
        self._store(data)

    def _attempt(self, task_id, number):
        if type(number) is not int or not 1 <= number <= MAX_ATTEMPTS:
            raise ValueError("Invalid or exhausted attempt count")
        group = self.groups[task_id].relative_to(self.workspace).as_posix()
        return safe_path(self.workspace, f"{group}/attempt-{number:02d}")

    def _readbacks(self, task_id, path):
        return [test_runs.output_check(path, check) for check in self.actions[task_id].checks]

    def _accepted(self, task_id, row):
        if row["state"] != "DONE":
            return False
        attempt = self._attempt(task_id, row["attempts"])
        proof = verify_completion.read_json(safe_path(attempt, "DONEPROOF.json"))
        input_root = safe_path(self.workspace, "inputs")
        return (all(test_runs.original_matches(input_root, self.inputs[name]) for name in self.actions[task_id].inputs)
                and proof.get("overall_status") == "verified"
                and not verify_completion.validate(proof)
                and not verify_completion.validate_against_plan(proof, self._proof_plan())
                and all(item["status"] == "PASS" for item in self._readbacks(task_id, attempt)))

    def _proof_plan(self):
        return {"request_id": self.request_id, "revision": self.revision, "tasks": list(self.tasks.values())}

    def _doneproof(self, task_id, readbacks, attempt):
        statements = self.tasks[task_id]["acceptance_criteria"]
        criteria = []
        for index, (statement, check) in enumerate(zip(statements, readbacks), 1):
            observed = check["status"] == "PASS"
            criteria.append({"id": f"C{index}", "statement": statement,
                             "status": "verified" if observed else "failed",
                             "evidence": [{"type": "artifact_readback", "revision": self.revision,
                                           "reference": (attempt / check["artifact"]).relative_to(self.workspace).as_posix(),
                                           "observed": "Independent comparison matched" if observed else "Independent comparison failed",
                                           "result": "pass" if observed else "fail"}]})
        verified = all(item["status"] == "verified" for item in criteria)
        proof = {"schema_version": "1.0", "request_id": self.request_id, "task_id": task_id,
                 "revision": self.revision, "overall_status": "verified" if verified else "failed",
                 "criteria": criteria}
        if verify_completion.validate(proof) or verify_completion.validate_against_plan(proof, self._proof_plan()):
            raise ValueError("Readback could not be bound to the reviewed criteria")
        test_runs.json_write(safe_path(attempt, "DONEPROOF.json"), proof)
        return verified

    def run(self, task_id, *, resume=False):
        self._grant(task_id, "resume" if resume else "execute")
        lock = safe_path(self.workspace, ".workflow.lock")
        lock.mkdir()
        try:
            data = self._load()
            row = data["tasks"][task_id]
            task = self.tasks[task_id]
            if row["state"] == "DONE":
                if not self._accepted(task_id, row):
                    raise ValueError("Existing accepted artifacts no longer match")
                return row
            if not all(self._accepted(dep, data["tasks"][dep]) for dep in task["depends_on"]):
                raise ValueError("Accept required task artifacts before executing dependants")
            if row["events"] and not resume:
                raise ValueError("An earlier attempt requires explicit resume")
            if not row["events"]:
                for preflight in ("RECEIVED", "REVIEWED", "PLANNED"):
                    self._event(data, task_id, preflight, "director")
            else:
                self._event(data, task_id, "RESUMED", "project-manager")
            self._event(data, task_id, "APPROVED", "director")
            binding = self.actions[task_id]
            input_root = safe_path(self.workspace, "inputs")
            if not all(test_runs.original_matches(input_root, self.inputs[name]) for name in binding.inputs):
                self._event(data, task_id, "BLOCKED", "security", reason="Prepared inputs changed")
                return row
            attempt = self._attempt(task_id, row["attempts"] + 1)
            attempt.mkdir(parents=True)
            row["attempts"] += 1
            trace_id = task.get("trace_id", f"{task_id}-{row['attempts']:02d}")
            self._event(data, task_id, "PREPARED", "developer", trace_id=trace_id,
                        command_id=binding.command_id, team=self.teams[task_id])
            self._event(data, task_id, "IN_PROGRESS", "developer")
            try:
                files = {name: safe_path(input_root, name) for name in binding.inputs}
                binding.execute(files, attempt)
                if not all(test_runs.original_matches(input_root, self.inputs[name]) for name in binding.inputs):
                    raise ValueError("The handler modified prepared inputs")
                integration_role = "developer" if self.teams[task_id]["profile"] == "LITE" else "integration"
                self._event(data, task_id, "INTEGRATION", integration_role,
                            artifact=attempt.relative_to(self.workspace).as_posix())
                readbacks = self._readbacks(task_id, attempt)
                test_runs.json_write(safe_path(attempt, "READBACK.json"), readbacks)
                self._event(data, task_id, "TESTING", "qa",
                            outcomes=[check["status"] for check in readbacks])
                passed = self._doneproof(task_id, readbacks, attempt)
            except (OSError, ValueError, RuntimeError) as error:
                self._event(data, task_id, "FAILED", "developer", reason=type(error).__name__)
                self._event(data, task_id, "REWORK", "qa")
                return row
            self._event(data, task_id, "REVIEW", "qa", review_mode="SAME_AGENT_REVIEW")
            self._event(data, task_id, "DONE" if passed else "REWORK", "release" if passed else "qa",
                        proof=(attempt / "DONEPROOF.json").relative_to(self.workspace).as_posix())
            return row
        finally:
            lock.rmdir()

    def rollback(self, task_id):
        self._grant(task_id, "rollback")
        lock = safe_path(self.workspace, ".workflow.lock")
        lock.mkdir()
        try:
            data = self._load()
            row = data["tasks"][task_id]
            if row["state"] != "DONE" or any(task_id in task["depends_on"] and data["tasks"][key]["attempts"]
                                               for key, task in self.tasks.items()):
                raise ValueError("Rollback requires an accepted task with no started dependants")
            self._event(data, task_id, "REWORK", "release", reason="Rolled back; prior artifacts retained")
            return row
        finally:
            lock.rmdir()
