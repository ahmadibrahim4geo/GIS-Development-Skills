"""Shared lifecycle state definitions, exit codes, and typed exceptions."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

LIFECYCLE_STATES = frozenset(
    {
        "UP_TO_DATE",
        "BUILT",
        "PASSED",
        "BUILD_FAILED",
        "VALIDATION_FAILED",
        "SYNCED_VERIFIED",
        "SYNC_FAILED_ROLLED_BACK",
        "OUTDATED",
        "RELOAD_REQUIRED",
        "NOT_INSTALLED",
        "UNSUPPORTED",
        "AUTH_REQUIRED",
        "MANUAL_ACTION_REQUIRED",
        "PREPARED_FOR_SUBMISSION",
        "PENDING_REVIEW",
        "PUBLISHED_VERIFIED",
        "NOT_APPLICABLE",
        "NETWORK_UNAVAILABLE",
        "LOCKED",
        "SECRET_LEAK_BLOCKED",
        "ROLLED_BACK",
        "NOT_RUN",
    }
)

EXIT_OK = 0
EXIT_BUILD_OR_VALIDATION_FAILED = 2
EXIT_PARTIAL_SYNC_ROLLED_BACK = 3
EXIT_APPROVAL_OR_MANUAL_REQUIRED = 4
EXIT_LOCK_OR_CONFIG_ERROR = 5

REDISTRIBUTION_ALLOWED_SPDX = frozenset(
    {
        "MIT",
        "APACHE-2.0",
        "BSD-2-CLAUSE",
        "BSD-3-CLAUSE",
        "ISC",
        "CC0-1.0",
        "UNLICENSE",
        "MPL-2.0",
        "LGPL-2.1-OR-LATER",
        "LGPL-3.0-OR-LATER",
        "ZLIB",
    }
)


class LifecycleError(RuntimeError):
    """Base error carrying an explicit lifecycle state and process exit code."""

    def __init__(self, message: str, *, state: str = "BUILD_FAILED", exit_code: int = EXIT_BUILD_OR_VALIDATION_FAILED):
        super().__init__(message)
        self.state = state if state in LIFECYCLE_STATES else "BUILD_FAILED"
        self.exit_code = exit_code


class ValidationFailedError(LifecycleError):
    def __init__(self, message: str):
        super().__init__(message, state="VALIDATION_FAILED", exit_code=EXIT_BUILD_OR_VALIDATION_FAILED)


class SecretLeakError(LifecycleError):
    def __init__(self, message: str):
        super().__init__(message, state="SECRET_LEAK_BLOCKED", exit_code=EXIT_BUILD_OR_VALIDATION_FAILED)


class LockTimeoutError(LifecycleError):
    def __init__(self, message: str):
        super().__init__(message, state="LOCKED", exit_code=EXIT_LOCK_OR_CONFIG_ERROR)


class ConfigError(LifecycleError):
    def __init__(self, message: str):
        super().__init__(message, state="VALIDATION_FAILED", exit_code=EXIT_LOCK_OR_CONFIG_ERROR)


class ApprovalRequiredError(LifecycleError):
    def __init__(self, message: str, *, state: str = "MANUAL_ACTION_REQUIRED"):
        super().__init__(message, state=state, exit_code=EXIT_APPROVAL_OR_MANUAL_REQUIRED)


@dataclass(frozen=True)
class PlatformConfig:
    """Declarative platform target definition parsed from platforms.json."""

    id: str
    display_name: str
    enabled: bool
    phase_target: str
    phase_status: str
    adapter: str
    output_dir: str
    bundle_dir: str = ""
    manifest_path: str = ""
    artifacts_dir: str = ""
    parity_report_path: str = ""
    archive_name: str = ""
    raw: dict[str, Any] = field(default_factory=dict)


@dataclass
class AdapterContext:
    """Execution context handed cleanly to adapters without secret leaks."""

    repo_root: Path
    version: str
    source_commit: str
    source_digest: str
    bundle_digest: str
    plugin_id: str
    suite_name: str
    source_map: dict[str, Any]
    sync_config: dict[str, Any]
    owner_config: dict[str, Any]
    owner_config_source: str = "none"
    force: bool = False
    is_ci: bool = False
    publish_approved: bool = False
