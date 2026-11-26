"""Unified Plugin Lifecycle orchestration CLI (replaces ad-hoc packaging)."""

from __future__ import annotations

import argparse
import importlib
import importlib.util
import json
import os
import re
import sys
import time
from pathlib import Path
from typing import Any

if __name__ == "__main__" and not __package__:
    _pkg_dir = Path(__file__).resolve().parents[1]
    _spec = importlib.util.spec_from_file_location(
        "plugin_system",
        _pkg_dir / "__init__.py",
        submodule_search_locations=[str(_pkg_dir)],
    )
    if _spec is None or _spec.loader is None:
        raise RuntimeError("Unable to initialize plugin_system package context")
    _pkg = importlib.util.module_from_spec(_spec)
    sys.modules["plugin_system"] = _pkg
    _spec.loader.exec_module(_pkg)
    sys.exit(importlib.import_module("plugin_system.core.pipeline").main())

from .builder import build_platform_transactionally
from .hashing import compute_digests, resolve_git_commit
from .inventory import collect_canonical_inventory
from .lock import ProjectLock
from .models import (
    AdapterContext,
    ConfigError,
    EXIT_APPROVAL_OR_MANUAL_REQUIRED,
    EXIT_BUILD_OR_VALIDATION_FAILED,
    EXIT_LOCK_OR_CONFIG_ERROR,
    EXIT_OK,
    EXIT_PARTIAL_SYNC_ROLLED_BACK,
    LifecycleError,
)
from .catalogs import check_repo_client_catalogs, render_platform_readme, sync_repo_client_catalogs
from .parity import write_root_plugins_index
from .registry import list_platform_configs, load_adapter, load_platforms_registry
from .validators import read_semver_version, scan_files_for_secrets, validate_canonical_repository
from ..release.release_manager import prepare_releases, publish_releases
from ..sync.rollback import snapshot_known_good
from ..sync.sync_manager import load_owner_config, sync_platforms_transactionally


def _load_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise ConfigError(f"Missing required configuration file: {path}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ConfigError(f"Invalid JSON configuration {path}: {exc}") from exc


def _next_report_prefix(report_dir: Path) -> str:
    highest = -1
    if report_dir.is_dir():
        for entry in report_dir.iterdir():
            m = re.match(r"^(\d{3})_", entry.name)
            if m:
                highest = max(highest, int(m.group(1)))
    return f"{highest + 1:03d}"


def _write_plugins_root_readme(plugins_root: Path, version: str, source_commit: str, platforms_summary: dict[str, Any]) -> None:
    lines = [
        "# GIS Development Skills — Generated Plugin Packages / حزم الإضافات المولدة",
        "",
        f"- **Version:** `{version}` (`{source_commit}`)",
        "- **Canonical Source:** [Repository README](../README.md) · [AGENTS Policy](../AGENTS.md) · [Lifecycle Architecture](../plugin-system/README.md)",
        "- **Important Rule:** Do not edit files in this folder by hand. Regenerate from canonical sources via `Update-All-Plugins.ps1` (or `python -B plugin-system/core/pipeline.py`).",
        "",
        "| Platform | State | Phase Status | Notes |",
        "|---|---|---|---|",
    ]
    for pid, pinfo in platforms_summary.items():
        lines.append(f"| `{pid}` | `{pinfo.get('state')}` | `{pinfo.get('phase_status')}` | {pinfo.get('notes', '')} |")
    lines.extend(
        [
            "",
            "## العربية / Quick Arabic Guide",
            "",
            "- هذا المجلد يُبنى آليًا من مستودع المصدر الواحد (`skills/` و`references/` و`schemas/`).",
            "- تدعم المنظومة حزمة **`portable-agent-plugin`** (من `P02`) إلى جانب المحولات الست المفعلة للعملاء (`codex`, `chatgpt`, `claude-code`, `claude-ai`, `antigravity`, `cursor`) في `P09`.",
            "- أرشيفات `.zip` الكبيرة تُبنى محليًا داخل `*/artifacts/` وهي مستبعدة من التتبع في Git للحفاظ على خفة المستودع.",
            "",
        ]
    )
    plugins_root.mkdir(parents=True, exist_ok=True)
    (plugins_root / "README.md").write_text("\n".join(lines), encoding="utf-8", newline="\n")


def _write_lifecycle_report(report_dir: Path, payload: dict[str, Any], *, label: str = "PLUGIN_LIFECYCLE") -> tuple[Path, Path]:
    report_dir.mkdir(parents=True, exist_ok=True)
    prefix = _next_report_prefix(report_dir)
    json_path = report_dir / f"{prefix}_{label}.json"
    md_path = report_dir / f"{prefix}_{label}.md"
    json_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")

    md_lines = [
        f"# Plugin Lifecycle Run `{prefix}_{label}`",
        "",
        f"- **Run ID:** `{payload['run_id']}`",
        f"- **Mode:** `{payload['mode']}`",
        f"- **Version:** `{payload['version']}`",
        f"- **Source Commit:** `{payload['source_commit']}`",
        f"- **Source Digest:** `{payload['source_digest']}`",
        f"- **Overall State:** `{payload['overall_state']}` (Exit `{payload['exit_code']}`)",
        "",
        "| Platform | State | Phase Status | Bundle SHA-256 | Notes |",
        "|---|---|---|---|---|",
    ]
    for pid, pinfo in payload.get("platforms", {}).items():
        md_lines.append(
            f"| `{pid}` | `{pinfo.get('state')}` | `{pinfo.get('phase_status')}` | `{pinfo.get('bundle_sha256') or '-'}` | {pinfo.get('notes', '')} |"
        )
    md_path.write_text("\n".join(md_lines) + "\n", encoding="utf-8", newline="\n")
    return json_path, md_path


def run_pipeline(
    repo_root: Path,
    *,
    mode: str = "full",
    selected_platforms: list[str] | None = None,
    force: bool = False,
    rollback_version: str | None = None,
    platforms_config_path: Path | None = None,
    owner_config_path: Path | None = None,
    write_report: bool = True,
    report_label: str = "PLUGIN_LIFECYCLE",
) -> dict[str, Any]:
    root = Path(repo_root).resolve()
    plugin_sys = root / "plugin-system"
    source_map = _load_json(plugin_sys / "config" / "source-map.json")
    sync_config = _load_json(plugin_sys / "config" / "plugin-sync.config.json")
    registry_data = load_platforms_registry(root, registry_path=platforms_config_path)
    all_configs = [cfg for cfg in list_platform_configs(root, registry_data) if cfg.enabled]

    if selected_platforms:
        wanted = set(selected_platforms)
        known = {cfg.id for cfg in all_configs}
        unknown = sorted(wanted - known)
        if unknown:
            raise ConfigError(f"Unknown platform target(s): {', '.join(unknown)}")
        configs = [cfg for cfg in all_configs if cfg.id in wanted]
    else:
        configs = all_configs

    adapters = [load_adapter(root, cfg) for cfg in configs]
    lock_path = root / sync_config.get("lockFileRelativePath", ".plugin-lock/update.lock.json")
    timeout_sec = float(sync_config.get("lockTimeoutSeconds", 30))
    stale_sec = float(sync_config.get("lockStaleSeconds", 600))

    with ProjectLock(lock_path, timeout_seconds=timeout_sec, stale_seconds=stale_sec):
        version = read_semver_version(root)
        commit = resolve_git_commit(root)
        inventory_data = collect_canonical_inventory(root, source_map)
        # Check secrets BEFORE bundling or computing final outputs.
        scan_files_for_secrets(inventory_data["bundle_files"] + inventory_data["governance_files"], root)
        digests = compute_digests(inventory_data)
        owner_cfg, owner_source = load_owner_config(sync_config, override_path=owner_config_path)
        is_ci = os.environ.get("GITHUB_ACTIONS", "").lower() == "true"

        context = AdapterContext(
            repo_root=root,
            version=version,
            source_commit=commit,
            source_digest=digests["source_digest"],
            bundle_digest=digests["bundle_digest"],
            plugin_id=str(registry_data.get("plugin_id", "ahmadibrahim4geo.gis-development-skills")),
            suite_name=str(registry_data.get("suite_name", "GIS Development Skills")),
            source_map=source_map,
            sync_config=sync_config,
            owner_config=owner_cfg,
            owner_config_source=owner_source,
            force=force,
            is_ci=is_ci,
            publish_approved=(mode == "publish"),
        )

        platform_results: dict[str, Any] = {}
        exit_code = EXIT_OK
        overall_state = "PASSED"

        if mode == "status":
            for ad in adapters:
                platform_results[ad.config.id] = ad.status(context)
            active_states = [
                v["state"]
                for v in platform_results.values()
                if str(v.get("phase_status", "")).startswith("ACTIVE_") or v.get("state") not in {"NOT_RUN"}
            ]
            overall_state = active_states[0] if len(set(active_states)) == 1 else ("UP_TO_DATE" if active_states and all(s == "UP_TO_DATE" for s in active_states) else "PASSED")
        elif mode == "rollback":
            for ad in adapters:
                platform_results[ad.config.id] = ad.rollback(context, rollback_version)
            overall_state = "ROLLED_BACK"
        elif mode == "publish":
            for ad in adapters:
                platform_results[ad.config.id] = ad.status(context)
            publish_releases(adapters, context)
            overall_state = "PUBLISHED_VERIFIED"
        else:
            # Canonical validation mandatory in check-only, build-only, full, prepare-release
            validate_canonical_repository(root)

            def _is_active(cfg) -> bool:
                return str(cfg.phase_status).startswith("ACTIVE_") or bool(cfg.raw.get("build_in_p02", False))

            # Save rollback snapshot of existing active built directories prior to rebuild swap
            if mode != "check-only":
                retention = int(sync_config.get("retentionCount", registry_data.get("default_retention", 3)))
                rollback_rel = sync_config.get("rollbackDirectoryRelativePath", ".plugin-local/rollback")
                for ad in adapters:
                    if _is_active(ad.config):
                        existing_dir = root / ad.config.bundle_dir
                        existing_manifest = root / ad.config.manifest_path
                        if existing_dir.is_dir() and existing_manifest.is_file():
                            try:
                                prev_ver = json.loads(existing_manifest.read_text(encoding="utf-8")).get("version", version)
                            except (OSError, json.JSONDecodeError):
                                prev_ver = version
                            st_now = ad.status(context).get("state")
                            if st_now != "UP_TO_DATE" or force:
                                snapshot_known_good(root, ad.config.id, prev_ver, existing_dir, retention=retention, rollback_rel=rollback_rel)

            for ad in adapters:
                platform_results[ad.config.id] = build_platform_transactionally(ad, context, check_only=(mode == "check-only"))

            if mode == "full" and sync_config.get("autoSyncLocal", True):
                active_adapters = [ad for ad in adapters if _is_active(ad.config)]
                sync_outcome = sync_platforms_transactionally(active_adapters, context)
                for pid, sinfo in sync_outcome["platforms"].items():
                    platform_results[pid]["sync"] = sinfo
                if sync_outcome["partial_failure"]:
                    exit_code = EXIT_PARTIAL_SYNC_ROLLED_BACK
                    overall_state = "SYNC_FAILED_ROLLED_BACK"

            if mode == "prepare-release":
                rel_outcome = prepare_releases(adapters, context)
                for pid, rinfo in rel_outcome.items():
                    platform_results[pid]["release"] = rinfo
                overall_state = "PREPARED_FOR_SUBMISSION"

            if exit_code == EXIT_OK and mode != "prepare-release":
                active_states = [
                    platform_results[ad.config.id]["state"]
                    for ad in adapters
                    if _is_active(ad.config)
                ]
                stale_catalogs = check_repo_client_catalogs(root, context, configs) if mode == "check-only" else []
                if mode == "check-only" and (any(s != "UP_TO_DATE" for s in active_states) or stale_catalogs):
                    overall_state = "VALIDATION_FAILED" if "VALIDATION_FAILED" in active_states else "OUTDATED"
                    exit_code = EXIT_BUILD_OR_VALIDATION_FAILED
                    if stale_catalogs:
                        platform_results["_marketplace_catalogs"] = {
                            "platform": "_marketplace_catalogs",
                            "state": "OUTDATED",
                            "phase_status": "ACTIVE_P09",
                            "stale_files": stale_catalogs,
                            "notes": "Tracked marketplace or Cursor rule files require regeneration via Update-All-Plugins.ps1.",
                        }
                elif active_states and all(s == "UP_TO_DATE" for s in active_states) and not stale_catalogs:
                    overall_state = "UP_TO_DATE"
                elif any(s == "BUILT" for s in active_states):
                    overall_state = "BUILT"

            if mode != "check-only":
                plugins_root = root / "GIS-Development-Skills-Plugins"
                # Ensure portable target also has bilingual README alongside client targets.
                for ad in adapters:
                    if ad.config.id == "portable" and ad.config.output_dir:
                        out_root = root / ad.config.output_dir
                        out_root.mkdir(parents=True, exist_ok=True)
                        (out_root / "README.md").write_text(
                            render_platform_readme(
                                ad.config,
                                context,
                                {
                                    "supports_hooks": False,
                                    "install_note_en": "Extract `artifacts/gis-development-suite.zip` or copy `plugin/` directly into any Agent Skills-compatible environment.",
                                    "install_note_ar": "فك ضغط `artifacts/gis-development-suite.zip` أو انسخ مجلد `plugin/` إلى أي عميل يدعم Agent Skills.",
                                },
                            ),
                            encoding="utf-8",
                            newline="\n",
                        )
                sync_repo_client_catalogs(root, context, configs)
                # Merge with existing index platforms when filtering with --platform
                index_file = plugins_root / "index.json"
                merged_summary: dict[str, Any] = {}
                if selected_platforms and index_file.is_file():
                    try:
                        merged_summary = json.loads(index_file.read_text(encoding="utf-8")).get("platforms", {})
                    except (OSError, json.JSONDecodeError):
                        merged_summary = {}
                for pid, pinfo in platform_results.items():
                    merged_summary[pid] = pinfo
                write_root_plugins_index(
                    plugins_root,
                    plugin_id=context.plugin_id,
                    version=version,
                    source_commit=commit,
                    source_digest=digests["source_digest"],
                    bundle_digest=digests["bundle_digest"],
                    platforms_summary=merged_summary,
                )
                _write_plugins_root_readme(plugins_root, version, commit, merged_summary)

        payload = {
            "schema_version": "1.0",
            "run_id": time.strftime("%Y%m%dT%H%M%SZ", time.gmtime()),
            "mode": mode,
            "version": version,
            "source_commit": commit,
            "source_digest": digests["source_digest"],
            "bundle_digest": digests["bundle_digest"],
            "bundle_file_count": digests["bundle_file_count"],
            "exit_code": exit_code,
            "overall_state": overall_state,
            "owner_config_source": owner_source,
            "platforms": platform_results,
        }

        if write_report and mode not in {"status", "check-only"}:
            report_dir = root / sync_config.get("reportDirectoryRelativePath", "reports/plugin-lifecycle")
            jp, mp = _write_lifecycle_report(report_dir, payload, label=report_label)
            payload["report_json"] = str(jp.relative_to(root).as_posix())
            payload["report_md"] = str(mp.relative_to(root).as_posix())

        return payload


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[2])
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument("--check-only", action="store_true")
    mode_group.add_argument("--build-only", action="store_true")
    mode_group.add_argument("--status", action="store_true")
    mode_group.add_argument("--rollback", action="store_true")
    mode_group.add_argument("--prepare-release", action="store_true")
    mode_group.add_argument("--publish", action="store_true")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--platform", action="append", default=[], help="Comma-separated or repeated target platform IDs")
    parser.add_argument("--version", help="Target version for --rollback")
    parser.add_argument("--platforms-config", type=Path, default=None)
    parser.add_argument("--owner-config", type=Path, default=None)
    parser.add_argument("--report-label", default="PLUGIN_LIFECYCLE")
    parser.add_argument("--no-report", action="store_true")
    parser.add_argument("--json", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    mode = "full"
    if args.check_only:
        mode = "check-only"
    elif args.build_only:
        mode = "build-only"
    elif args.status:
        mode = "status"
    elif args.rollback:
        mode = "rollback"
    elif args.prepare_release:
        mode = "prepare-release"
    elif args.publish:
        mode = "publish"

    platforms: list[str] = []
    for raw in args.platform:
        for item in raw.split(","):
            item = item.strip()
            if item:
                platforms.append(item)

    try:
        result = run_pipeline(
            args.repo_root,
            mode=mode,
            selected_platforms=platforms or None,
            force=args.force,
            rollback_version=args.version,
            platforms_config_path=args.platforms_config,
            owner_config_path=args.owner_config,
            write_report=not args.no_report,
            report_label=args.report_label,
        )
        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(
                f"Plugin Lifecycle [{result['mode']}]: {result['overall_state']} | version={result['version']} | digest={result['source_digest'][:12]}"
            )
            for pid, pinfo in result["platforms"].items():
                print(f"  - {pid}: {pinfo.get('state')} ({pinfo.get('phase_status')}) :: {pinfo.get('notes', '')}")
        return int(result["exit_code"])
    except LifecycleError as exc:
        err_payload = {"status": "ERROR", "state": exc.state, "exit_code": exc.exit_code, "error": str(exc)}
        if args.json:
            print(json.dumps(err_payload, indent=2, ensure_ascii=False))
        else:
            print(f"Plugin Lifecycle ERROR [{exc.state}] (exit {exc.exit_code}): {exc}", file=sys.stderr)
        return int(exc.exit_code)
    except Exception as exc:  # noqa: BLE001 — bounded deterministic error handling
        err_payload = {"status": "ERROR", "state": "BUILD_FAILED", "exit_code": EXIT_BUILD_OR_VALIDATION_FAILED, "error": str(exc)}
        if args.json:
            print(json.dumps(err_payload, indent=2, ensure_ascii=False))
        else:
            print(f"Plugin Lifecycle unexpected error: {exc}", file=sys.stderr)
        return EXIT_BUILD_OR_VALIDATION_FAILED
