"""Inspect prerequisites for a selected skill without installing or running it."""

import re
import shutil
from pathlib import Path

if __package__:
    from . import project_structure, skill_intake
else:
    import project_structure
    import skill_intake


SUITE = Path(__file__).resolve().parents[1]
IDENTIFIER = re.compile(r"[a-z][a-z0-9-]{0,63}\Z")
COMMAND = re.compile(r"[a-zA-Z0-9][a-zA-Z0-9_.+-]{0,63}\Z")
# Optional providers are alternatives. Presence never substitutes for a smoke test.
PROFILES = {
    "ui-ux-pro-max": (("scripts/search.py", "data/catalog-summary.json"),
                      ("python", "python3", "py"), ()),
    "craft-anything": ((), ("craft-anything-cli",), ("craft-mcp",)),
    "reverse-engineer-anything": ((), (), ("rea-mcp", "rea-cli")),
    "github-delivery": ((), ("gh",), ("github-connector",)),
}


def locate(skill, explicit, project, suite):
    if explicit is not None:
        return explicit.expanduser().absolute()
    locations = (suite / "skills", project / ".agents/skills", project / ".claude/skills",
                 project / ".github/skills", Path.home() / ".agents/skills",
                 Path.home() / ".codex/skills", Path.home() / ".claude/skills")
    return next((parent / skill for parent in locations if (parent / skill / "SKILL.md").is_file()), None)


def instructions(directory, filename, *, require_header):
    if directory is None:
        return False
    if any(project_structure.is_link(path) for path in (*reversed(directory.parents), directory)):
        raise ValueError("Choose an inspectable local skill directory without links.")
    path = project_structure.safe_path(directory.resolve(), filename)
    if not path.is_file() or path.stat().st_size > project_structure.MAX_FILE_BYTES:
        return False
    if require_header:
        with path.open("rb") as handle:
            content = handle.read(project_structure.MAX_FILE_BYTES + 1)
        try:
            text = content.decode("utf-8-sig")
        except UnicodeError:
            return False
        return len(content) <= project_structure.MAX_FILE_BYTES and skill_intake.skill_header(text, path)
    return True


def inspect(project, skill, *, skill_dir=None, require_files=(), require_commands=(),
            require_capabilities=(), available_capabilities=(), source_reviewed=False,
            which=shutil.which, suite=SUITE):
    if not IDENTIFIER.fullmatch(skill):
        raise ValueError("Use a skill name in lowercase kebab case.")
    if any(not COMMAND.fullmatch(item) for item in require_commands):
        raise ValueError("Use command names without paths or arguments.")
    if any(not IDENTIFIER.fullmatch(item) for item in (*require_capabilities, *available_capabilities)):
        raise ValueError("Use lowercase capability identifiers.")

    default_files, providers, capabilities = PROFILES.get(skill, ((), (), ()))
    publishing = skill == "github-delivery"
    if publishing and skill_dir is not None:
        raise ValueError("GitHub delivery uses the repository publishing guide.")
    directory = suite if publishing else locate(skill, skill_dir, project, suite)
    filename = "PUBLISHING.md" if publishing else "SKILL.md"
    bundled = publishing or (directory is not None and directory.parent.resolve() == (suite / "skills").resolve())
    quarantined = directory is not None and any(part.casefold() == "new skill" for part in directory.resolve().parts)
    readable = instructions(directory, filename, require_header=not publishing)
    scope = "QUARANTINED" if quarantined else "BUNDLED" if bundled else (
        "REVIEWED_BY_HOST" if source_reviewed else "SOURCE_REVIEW_REQUIRED")

    files = []
    for name in dict.fromkeys((*default_files, *require_files)):
        if directory is None:
            project_structure.safe_path(project, name)
        path = project_structure.safe_path(directory.resolve(), name) if directory else None
        files.append({"file": name, "present": bool(path is not None and path.is_file())})
    found = {name: bool(which(name)) for name in dict.fromkeys((*providers, *require_commands))}
    declared = set(available_capabilities)
    missing = ([filename] if not readable else []) + [row["file"] for row in files if not row["present"]]
    missing.extend(name for name in require_commands if not found[name])
    missing.extend(name for name in require_capabilities if name not in declared)
    if (providers or capabilities) and not (any(found[name] for name in providers) or declared.intersection(capabilities)):
        missing.append(" or ".join((*providers, *capabilities)))

    if quarantined:
        status = "QUARANTINED"
    elif missing:
        status = "MISSING_REQUIREMENTS"
    elif scope == "SOURCE_REVIEW_REQUIRED":
        status = scope
    else:
        status = "VERIFY_REQUIRED"
    return {
        "skill": skill, "status": status, "source": scope,
        "instruction_file": str(directory / filename) if directory else None,
        "instructions_readable": readable, "files": files, "commands_found_on_path": found,
        "host_declared_capabilities": sorted(declared.intersection((*capabilities, *require_capabilities))),
        "missing_requirements": list(dict.fromkeys(missing)), "independent_work_can_continue": True,
        "runtime_compatibility": "NOT CHECKED", "license_and_permissions": "HOST REVIEW REQUIRED",
        "functional_test": "NOT RUN", "execution_authorized": False,
        "next_action": "Review missing capabilities, source, terms and permissions. Verify the actual version, schema and behavior in the host before use.",
    }
