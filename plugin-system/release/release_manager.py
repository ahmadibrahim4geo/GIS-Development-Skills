"""Release artifact staging (`-PrepareRelease`) vs approval-gated publishing (`-Publish`)."""

from __future__ import annotations

from typing import Any

from ..core.models import AdapterContext, ApprovalRequiredError


def prepare_releases(adapters: list[Any], context: AdapterContext) -> dict[str, Any]:
    outcomes: dict[str, Any] = {}
    for adapter in adapters:
        outcomes[adapter.config.id] = adapter.prepare_release(context)
    return outcomes


def publish_releases(adapters: list[Any], context: AdapterContext) -> dict[str, Any]:
    """Strictly refuse public or remote store publishing without explicit owner & CLI consent."""
    allow_public = bool(context.owner_config.get("allowPublicPublish", False))
    allow_remote = bool(context.owner_config.get("allowRemoteUpdate", False))
    if not context.publish_approved or not (allow_public or allow_remote):
        raise ApprovalRequiredError(
            "Publishing is disabled by default; requires explicit -Publish consent AND external owner-config authorization.",
            state="MANUAL_ACTION_REQUIRED",
        )
    outcomes: dict[str, Any] = {}
    for adapter in adapters:
        outcomes[adapter.config.id] = adapter.update_owner_remote(context)
    return outcomes
