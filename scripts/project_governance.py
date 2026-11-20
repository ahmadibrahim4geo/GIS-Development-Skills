#!/usr/bin/env python3
"""Project governance for GIS Development Skills target projects.

Standard-library-only. No downloads, dependency installation, GIS processing or
untrusted skill execution. Mutating commands require an explicit CLI invocation.
The hosting agent remains responsible for actual user approval and native tests.
"""
import argparse
import json
import os
import re
import shutil
import sys
from pathlib import Path
from urllib.parse import urlparse

MANAGED = "<!-- GIS-Development-Skills:managed-project-governance-v1 -->"
STRUCTURE_MARKER = "<!-- GIS-Development-Skills:managed-structure-v1 -->"
DIRECTORIES = {
    "agent": "Project-specific policies and engineering organization",
    "plans": "Numbered development plans and revision history",
    "plans/active": "Open, proposed, and in-progress development plans",
    "plans/archive": "Completed plans with linked evidence (not deleted)",
    "reports": "Engineering, inspection, and verification reports",
    "context": "Short project map and current handoff state",
    "testing data": "USER-OWNED test fixtures; read-only by default; never use for outputs",
    "testing results": "GENERATED test runs, logs, screenshots, and output readback",
    "New Skill": "External skill candidates and promotion records, not an active skill path",
    "New Skill/candidates": "Untrusted skill metadata pending license/security review",
    "New Skill/approved": "Only separately reviewed and authorized skill copies",
    "New Skill/promotion": "Evidence and requests to promote a skill into the main suite",
    "dist": "Build/distribution artifacts, not source",
    "dist/user-testing": "User-test builds only after appropriate build verification",
}
ROOT_FILES = {
    "AGENTS.md": "Agent instructions and project execution/permission boundaries",
    "README.md": "Project introduction, setup, and usage",
    "PROJECT_STRUCTURE.md": "Living catalog of project directories and root files",
    "PROJECT_MANIFEST.json": "Project inventory or manifest (if used by the host project)",
    ".gis-project-governance.json": "Project-local folder descriptions and governance version",
    ".gitignore": "Git exclusions for generated outputs and private test data",
    ".gitattributes": "Git file attributes",
    "LICENSE": "Source license",
    "pyproject.toml": "Python packaging and tool configuration",
    "package.json": "JavaScript package scripts and dependencies",
    "CMakeLists.txt": "CMake build definition",
    "requirements.txt": "Python dependency requirements",
}
IGNORED_WALK = {".git", ".venv", "venv", "node_modules", "__pycache__",
                ".pytest_cache", ".mypy_cache", ".idea", ".vs", ".next",
                "bin", "obj", "build", "dist", "testing data",
                "testing results", ".agent-development-log"}
CONFIG = ".gis-project-governance.json"


def safe_path(root, relative):
    """Only an existing or future non-symlinked path below the project."""
    if not isinstance(relative, str) or not relative.strip():
        raise ValueError("Nonempty relative path required")
    if "\x00" in relative or "\\" in relative or ":" in relative:
        raise ValueError("Use a POSIX-style project-relative path")
    candidate = Path(relative)
    if candidate.is_absolute() or any(x in (".", "..") for x in candidate.parts):
        raise ValueError("Absolute and traversing paths are prohibited")
    root = root.resolve()
    full = root / candidate
    if not full.resolve().is_relative_to(root):
        raise ValueError("Path escapes project root")
    for part in (root / candidate).relative_to(root).parts:
        root = root / part
        if root.is_symlink():
            raise ValueError("Symlinked paths are not permitted")
    return full


def slug(title):
    cleaned = re.sub(r"[^a-zA-Z0-9_\-\u0600-\u06FF]+", "-", title).strip("-_")
    if not cleaned:
        raise ValueError("Title requires letters or digits")
    return cleaned[:70]


def read_json(path, default):
    if not path.exists():
        return default
    obj = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(obj, dict):
        raise ValueError(f"Invalid JSON object: {path}")
    return obj


def write_new(path, content):
    """Never overwrite user-authored files."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="\n") as handle:
        handle.write(content)


def save_json(path, obj):
    """Atomic replacement for a file managed by this CLI only."""
    if path.is_symlink():
        raise ValueError("Refusing to overwrite a symlink")
    temporary = path.with_name(path.name + ".tmp")
    if temporary.exists():
        raise FileExistsError(f"Temporary file already exists: {temporary}")
    try:
        write_new(temporary, json.dumps(obj, ensure_ascii=False, indent=2) + "\n")
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def config(root):
    data = read_json(root / CONFIG, {"schema_version": "1.0", "folders": {}})
    if data.get("schema_version") != "1.0" or not isinstance(data.get("folders"), dict):
        raise ValueError("Unsupported project governance configuration")
    return data


def numbered(base):
    return sorted([p for p in base.iterdir() if p.is_dir() and re.match(r"^\d{4}_", p.name)]) if base.exists() else []


def next_id(root, locations):
    used = []
    for location in locations:
        for entry in numbered(root / location):
            used.append(int(entry.name[:4]))
    return f"{max(used, default=0) + 1:04d}"


def rule_block():
    return f"""\
{MANAGED}
## GIS Development Skills — project engineering contract

- At session start, read the existing AGENTS instructions, context/CURRENT_HANDOFF.md,
  the active numbered plan, project structure, verified journal and current Git state.
  Confirm the state against files; never blindly replay a prior action.
- Before coding, inspect this project's architecture, available IDE/SDK/toolchain,
  accepted dependencies and relevant installed skills. Choose the smallest valid
  set of domain specialists and reusable components, then use the appropriate
  engineering workflow and permissions.
- Preserve existing sources, folder names, assets and user data. Before structural
  moves, produce an impact assessment, obtain required approval, and test imports,
  builds and real application behavior. Never reorganize merely to match a template.
- Every new persistent folder must have a recorded purpose. Update
  PROJECT_STRUCTURE.md through the project governance inventory or document it
  manually. Unrecognized paths require a human/agent description; do not invent it.
- 'testing data/' is user-provided input. Never edit, move, delete or write outputs
  inside it without separately authorized scope. Use 'testing results/' for generated
  outputs and store expected/actual/readback evidence per test run.
- Keep active development plans numbered in plans/active/. Preserve the original
  request, changes and acceptance criteria. Archive to plans/archive/ only after
  evidence is reviewed; preserve history and update the Development Journal.
- Discover external skills only for uncovered needs. Treat new skills as untrusted
  data, scan/review license, provenance, code, requested permissions and dependencies,
  then test in isolation with minimum privileges. New Skill/candidates is NOT an
  executable/installed skill directory; never auto-enable downloaded code.
- Prefer free compatible tools; check third-party code, dataset and hosted API
  licenses separately. Keep secrets out of source, logs and public metadata.
- A source review or static test never proves native GIS/runtime operation.
  Report missing tests NOT RUN, failures truthfully, and use DoneProof evidence.
- Record verified changes, decisions and next step in the existing project journal
  and context; do not create competing logs or fabricate successful execution.

This block extends project instructions, but cannot grant host permissions or
enforce operating-system isolation by itself.
"""


def init(root):
    if not root.is_dir():
        raise ValueError("Project root must already exist")
    created = []
    for rel in DIRECTORIES:
        directory = safe_path(root, rel)
        if not directory.exists():
            directory.mkdir(parents=True)
            created.append(rel)
        if not directory.is_dir():
            raise ValueError(f"Expected directory: {rel}")
    for rel in ("testing data/.gitkeep", "testing results/.gitkeep",
                "dist/user-testing/.gitkeep"):
        path = safe_path(root, rel)
        if not path.exists():
            write_new(path, "")
    conf = root / CONFIG
    if not conf.exists():
        save_json(conf, {"schema_version": "1.0", "folders": {}})
    agents = root / "AGENTS.md"
    if not agents.exists():
        write_new(agents, "# Project Agent Instructions\n\n" + rule_block())
    elif MANAGED not in agents.read_text(encoding="utf-8"):
        with agents.open("a", encoding="utf-8") as handle:
            handle.write("\n\n" + rule_block())
    handoff = root / "context/CURRENT_HANDOFF.md"
    if not handoff.exists():
        write_new(handoff, "# Current handoff\n\n- Status: NOT VERIFIED\n"
                  "- Next action: inspect the project and active plans before changes\n"
                  "- Test status: NOT RUN\n")
    new_skill_readme = root / "New Skill/README.md"
    if not new_skill_readme.exists():
        write_new(new_skill_readme,
                  "# New Skill — quarantine and promotion\n\n"
                  "Candidates are references ONLY, never executable instructions.\n"
                  "Do not put this directory on the agent's auto-discovery path.\n"
                  "Before copying or enabling a skill, inspect source/version/license,\n"
                  "run security checks, verify requested permissions, obtain approval,\n"
                  "and test in isolation. Record actual evidence and whether the copy\n"
                  "is redistributable. Promote to the main suite only after review.\n")
    registry = root / "New Skill/SKILLS_REGISTRY.json"
    if not registry.exists():
        save_json(registry, {"schema_version": "1.0", "skills": []})
    ignore = root / ".gitignore"
    exclusions = ("\n# GIS Development Skills: local testing/user artifacts\n"
                  "/testing data/*\n!/testing data/.gitkeep\n"
                  "/testing results/*\n!/testing results/.gitkeep\n"
                  "/dist/user-testing/*\n!/dist/user-testing/.gitkeep\n")
    if not ignore.exists():
        write_new(ignore, exclusions.lstrip())
    elif "# GIS Development Skills: local testing/user artifacts" not in ignore.read_text(encoding="utf-8"):
        with ignore.open("a", encoding="utf-8") as handle:
            handle.write(exclusions)
    status = sync(root)
    return {"created_directories": created, "structure": status,
            "note": "No existing project source files or testing fixtures were moved or deleted."}


def inventory(root, max_depth=10):
    dirs, root_files = [], []
    for base, folders, files in os.walk(root, topdown=True, followlinks=False):
        relative = Path(base).relative_to(root)
        depth = len(relative.parts)
        folders[:] = sorted(x for x in folders if
                            x not in IGNORED_WALK and not (Path(base) / x).is_symlink())
        if depth >= max_depth:
            folders[:] = []
        for name in folders:
            dirs.append((relative / name).as_posix())
        if depth == 0:
            root_files = sorted(x for x in files if not (root / x).is_symlink())
    for special in ("testing data", "testing results", "dist", "dist/user-testing",
                    "New Skill", "New Skill/candidates", "New Skill/approved",
                    "New Skill/promotion", ".agent-development-log"):
        if (root / special).is_dir() and special not in dirs:
            dirs.append(special)
    return sorted(set(dirs), key=str.casefold), root_files


def describe(rel, declared):
    if rel in declared:
        return declared[rel]["purpose"]
    if rel in DIRECTORIES:
        return DIRECTORIES[rel]
    return "NEEDS_DESCRIPTION — inspect and record this directory's purpose"


def structure_text(root, dirs, files, declared):
    lines = [STRUCTURE_MARKER, "# Project Structure",
             "", "Generated inventory of significant directories and root files.",
             "Descriptions marked NEEDS_DESCRIPTION require review, not guessing.",
             "Testing data belongs to the user; never modify its inputs by default.",
             "", "## Directories", "", "| Path | Purpose |", "| --- | --- |"]
    for rel in dirs:
        lines.append(f"| \u0060{rel}\u0060 | {describe(rel, declared).replace('|', '/')} |")
    lines += ["", "## Root files", "", "| Path | Purpose |", "| --- | --- |"]
    for name in files:
        lines.append(f"| \u0060{name}\u0060 | {ROOT_FILES.get(name, 'NEEDS_DESCRIPTION — inspect this root file')} |")
    lines += ["", "## Maintenance", "",
              "Register new persistent directories with register-folder and run sync.",
              "Review existing project build files before moving anything. Generated",
              "test outputs belong in testing results/, never in testing data/.", ""]
    return "\n".join(lines)


def sync(root):
    declared = config(root)["folders"]
    dirs, files = inventory(root)
    output = root / "PROJECT_STRUCTURE.md"
    text = structure_text(root, dirs, files, declared)
    if output.exists() and not output.read_text(encoding="utf-8").startswith(STRUCTURE_MARKER):
        return {"updated": False, "reason": "User-authored PROJECT_STRUCTURE.md preserved",
                "undocumented_directories": [x for x in dirs if x not in declared and x not in DIRECTORIES]}
    save_json(root / CONFIG, config(root))  # Keep structured config valid.
    if output.exists():
        temporary = output.with_suffix(".md.tmp")
        if temporary.exists():
            raise FileExistsError(temporary)
        try:
            write_new(temporary, text)
            os.replace(temporary, output)
        finally:
            if temporary.exists():
                temporary.unlink()
    else:
        write_new(output, text)
    return {"updated": True, "directories": len(dirs), "root_files": len(files),
            "undocumented_directories": [x for x in dirs if x not in declared and x not in DIRECTORIES]}


def register_folder(root, rel, purpose):
    folder = safe_path(root, rel)
    if not folder.is_dir():
        raise ValueError("Register an existing directory, not a proposed path")
    if not purpose.strip():
        raise ValueError("Directory purpose cannot be blank")
    data = config(root)
    data["folders"][rel] = {"purpose": purpose.strip()}
    save_json(root / CONFIG, data)
    return sync(root)


def new_plan(root, title, request):
    safe_path(root, "plans/active").mkdir(parents=True, exist_ok=True)
    sequence = next_id(root, ("plans/active", "plans/archive"))
    rel = f"plans/active/{sequence}_{slug(title)}"
    path = safe_path(root, rel)
    path.mkdir()
    write_new(path / "REQUEST.md", "# Original request\n\n" + request.strip() + "\n")
    write_new(path / "PLAN.md",
              f"# {title.strip()}\n\n## Objective\n\nTo be reviewed.\n\n"
              "## Scope and dependencies\n\nTo be assessed.\n\n"
              "## Acceptance criteria\n\nNot approved; add measurable results before execution.\n")
    save_json(path / "STATUS.json",
              {"id": sequence, "title": title.strip(), "status": "DRAFT",
               "revision": 1, "evidence": []})
    sync(root)
    return {"id": sequence, "path": rel, "status": "DRAFT", "approval": "NOT GRANTED"}


def find_plan(root, sequence):
    if not re.fullmatch(r"\d{4}", sequence):
        raise ValueError("Plan ID must be 4 digits")
    found = [p for p in numbered(root / "plans/active") if p.name.startswith(sequence + "_")]
    if len(found) != 1:
        raise ValueError("Exactly one active plan with this ID is required")
    return found[0]


def close_plan(root, sequence, evidence):
    plan = find_plan(root, sequence)
    proof = safe_path(root, evidence)
    if not proof.is_file() or proof.stat().st_size == 0:
        raise ValueError("A nonempty existing project-local evidence file is required")
    state = read_json(plan / "STATUS.json", {})
    if state.get("id") != sequence:
        raise ValueError("Plan metadata does not match plan ID")
    target = safe_path(root, "plans/archive") / plan.name
    if target.exists():
        raise FileExistsError("Archived plan already exists")
    state.update(status="ARCHIVED_WITH_REFERENCED_EVIDENCE", evidence=[evidence])
    save_json(plan / "STATUS.json", state)
    shutil.move(str(plan), str(target))
    sync(root)
    return {"path": target.relative_to(root).as_posix(),
            "note": "Evidence file presence checked, NOT its scientific/native validity. DoneProof and project journal remain required."}


def new_test_run(root, title):
    if not (root / "testing data").is_dir():
        raise ValueError("Run init first to create the user-owned testing data directory")
    sequence = next_id(root, ("testing results",))
    rel = f"testing results/{sequence}_{slug(title)}"
    path = safe_path(root, rel)
    path.mkdir(parents=True)
    write_new(path / "TEST_RUN.md",
              f"# Test run {sequence}: {title.strip()}\n\n"
              "Status: NOT RUN\n\nInput: ../testing data/ (read-only user fixtures)\n\n"
              "Expected result: TO DEFINE\n\nActual result: NOT RUN\n\n"
              "Tool versions, exact commands, output readback, and evidence: NOT RUN\n")
    return {"run": rel, "status": "NOT RUN",
            "input_folder": "testing data", "output_folder": rel}


def register_skill(root, name, source, purpose, revision, license_name):
    parsed = urlparse(source)
    if parsed.scheme != "https" or not parsed.netloc or parsed.username or parsed.password:
        raise ValueError("External skill source must be a public HTTPS URL")
    skills_path = root / "New Skill/SKILLS_REGISTRY.json"
    registry = read_json(skills_path, {"schema_version": "1.0", "skills": []})
    if registry.get("schema_version") != "1.0" or not isinstance(registry.get("skills"), list):
        raise ValueError("Invalid skill registry")
    if any(x.get("source") == source for x in registry["skills"]):
        raise ValueError("Skill source already registered")
    base = safe_path(root, "New Skill/candidates")
    base.mkdir(parents=True, exist_ok=True)
    sid = next_id(root, ("New Skill/candidates",))
    folder = base / f"{sid}_{slug(name)}"
    folder.mkdir()
    write_new(folder / "SOURCE.md",
              f"# Candidate: {name}\n\nSource: {source}\n\n"
              f"Upstream revision: {revision or 'NOT PINNED'}\n\n"
              f"Reported license: {license_name or 'UNVERIFIED'}\n\n"
              f"Purpose: {purpose}\n\nSecurity review: NOT RUN\n\n"
              "Status: CANDIDATE ONLY — no files fetched, no tools executed.\n")
    registry["skills"].append(
        {"id": sid, "name": name, "source": source,
         "revision": revision or None, "license": license_name or "UNVERIFIED",
         "purpose": purpose, "status": "CANDIDATE_UNREVIEWED",
         "path": folder.relative_to(root).as_posix(),
         "security_review": "NOT RUN", "runtime_test": "NOT RUN"})
    save_json(skills_path, registry)
    sync(root)
    return {"id": sid, "path": folder.relative_to(root).as_posix(),
            "status": "CANDIDATE_UNREVIEWED", "executed": False}


def audit(root):
    required = ["AGENTS.md", "PROJECT_STRUCTURE.md", "testing data", "testing results",
                "New Skill/SKILLS_REGISTRY.json", "plans/active", "plans/archive",
                "context/CURRENT_HANDOFF.md"]
    missing = [x for x in required if not (root / x).exists()]
    dirs, _ = inventory(root)
    defined = config(root)["folders"]
    active = [p.name for p in numbered(root / "plans/active")]
    unknown = [x for x in dirs if x not in DIRECTORIES and x not in defined]
    return {"project": str(root), "missing_required": missing,
            "undocumented_directories": unknown, "active_plans": active,
            "testing_data_user_owned": True, "testing_results_separate": True,
            "runtime_verification": "NOT RUN",
            "note": "Read-only structural check; it does not execute GIS, a build or a scanner."}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, default=Path("."))
    commands = parser.add_subparsers(dest="action", required=True)
    commands.add_parser("init")
    commands.add_parser("sync")
    commands.add_parser("audit")
    folder = commands.add_parser("register-folder")
    folder.add_argument("--path", required=True)
    folder.add_argument("--purpose", required=True)
    plan = commands.add_parser("new-plan")
    plan.add_argument("--title", required=True)
    source = plan.add_mutually_exclusive_group(required=True)
    source.add_argument("--request")
    source.add_argument("--request-file", type=Path)
    close = commands.add_parser("close-plan")
    close.add_argument("--id", required=True)
    close.add_argument("--evidence", required=True)
    run = commands.add_parser("new-test-run")
    run.add_argument("--name", required=True)
    skill = commands.add_parser("register-skill")
    skill.add_argument("--name", required=True)
    skill.add_argument("--source", required=True)
    skill.add_argument("--purpose", required=True)
    skill.add_argument("--revision", default="")
    skill.add_argument("--license", default="")
    opts = parser.parse_args(argv)
    root = opts.project.expanduser().resolve()
    try:
        if not root.is_dir():
            raise ValueError("Project must exist; this tool does not create an arbitrary project root")
        if opts.action == "init":
            result = init(root)
        elif opts.action == "sync":
            result = sync(root)
        elif opts.action == "audit":
            result = audit(root)
        elif opts.action == "register-folder":
            result = register_folder(root, opts.path, opts.purpose)
        elif opts.action == "new-plan":
            request = opts.request if opts.request is not None else opts.request_file.read_text(encoding="utf-8")
            if not request.strip():
                raise ValueError("Original request cannot be empty")
            result = new_plan(root, opts.title, request)
        elif opts.action == "close-plan":
            result = close_plan(root, opts.id, opts.evidence)
        elif opts.action == "new-test-run":
            result = new_test_run(root, opts.name)
        elif opts.action == "register-skill":
            result = register_skill(root, opts.name, opts.source,
                                    opts.purpose, opts.revision, opts.license)
        else:
            raise ValueError("Unrecognized action")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({"error": str(exc), "action": opts.action}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
