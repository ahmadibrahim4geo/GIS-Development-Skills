#!/usr/bin/env python3
"""Read-only GitHub repository metadata verifier for candidate engines.

Queries api.github.com only with redirect blocking, 1 MiB response cap, bounded
timeout, optional local disk caching, and strict state='metadata-only' output.
Never installs packages, clones repositories, or sends user prompts upstream.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import socket
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


OWNER_REPO_RE = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
DEFAULT_API_BASE = "https://api.github.com"
MAX_RESPONSE_BYTES = 1_048_576
DEFAULT_TIMEOUT_SECONDS = 12.0


class _NoRedirectHandler(urllib.request.HTTPRedirectHandler):
    """Refuse HTTP redirects so lookups cannot leave api.github.com."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):  # noqa: D401
        if fp is not None:
            fp.close()
        raise urllib.error.HTTPError(
            req.full_url,
            code,
            f"HTTP redirect {code} blocked by security policy",
            headers,
            None,
        )


def normalize_repo_slug(repo: str) -> str:
    """Validate and normalize an owner/repo GitHub identifier."""
    candidate = repo.strip()
    if candidate.startswith("https://github.com/"):
        candidate = candidate[len("https://github.com/") :].strip("/")
    if not OWNER_REPO_RE.fullmatch(candidate) or ".." in candidate.split("/"):
        raise ValueError(f"Invalid GitHub owner/repo slug: {repo!r}")
    return candidate


def _validate_api_base(api_base: str) -> str:
    parsed = urllib.parse.urlsplit(api_base.rstrip("/"))
    if parsed.scheme == "https" and parsed.netloc.casefold() == "api.github.com":
        return f"https://{parsed.netloc}"
    if parsed.scheme == "http" and parsed.hostname in {"127.0.0.1", "localhost"}:
        return f"http://{parsed.netloc}"
    raise ValueError(f"Disallowed metadata API base host: {api_base!r}")


def _cache_path_for(cache_dir: Path, slug: str) -> Path:
    digest = hashlib.sha256(slug.casefold().encode("utf-8")).hexdigest()
    return cache_dir / f"{digest}.json"


def _read_cache(cache_dir: Path, slug: str, ttl_seconds: int) -> dict[str, Any] | None:
    path = _cache_path_for(cache_dir, slug)
    if not path.is_file():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        cached_at = float(payload.get("_cached_epoch", 0))
    except (OSError, ValueError, TypeError):
        return None
    if ttl_seconds >= 0 and (time.time() - cached_at) > ttl_seconds:
        return None
    payload["cache_hit"] = True
    payload.pop("_cached_epoch", None)
    return payload


def _write_cache(cache_dir: Path, slug: str, record: dict[str, Any]) -> None:
    cache_dir.mkdir(parents=True, exist_ok=True)
    stored = dict(record)
    stored["_cached_epoch"] = time.time()
    _cache_path_for(cache_dir, slug).write_text(
        json.dumps(stored, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _unresolved_record(
    slug: str,
    reason: str,
    *,
    http_status: int | None = None,
    rate_limited: bool = False,
    retry_after: str | None = None,
) -> dict[str, Any]:
    return {
        "schema_version": "1.0",
        "repo": slug,
        "state": "unresolved",
        "reason": reason,
        "http_status": http_status,
        "rate_limited": rate_limited,
        "retry_after": retry_after,
        "license_verified": False,
        "integration_recommendation": "reference-only",
        "observed_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "security_warning": "Unresolved repository metadata cannot authorize reuse or execution.",
    }


def fetch_repo_metadata(
    repo: str,
    *,
    timeout: float = DEFAULT_TIMEOUT_SECONDS,
    cache_dir: Path | None = None,
    cache_ttl_seconds: int = 3600,
    _api_base: str = DEFAULT_API_BASE,
) -> dict[str, Any]:
    """Fetch bounded read-only GitHub repository metadata without redirects or auto-install."""
    slug = normalize_repo_slug(repo)
    base = _validate_api_base(_api_base)
    if cache_dir is not None:
        cached = _read_cache(Path(cache_dir), slug, cache_ttl_seconds)
        if cached is not None:
            return cached

    url = f"{base}/repos/{slug}"
    headers = {
        "User-Agent": "GIS-Development-Skills-Metadata/1.0",
        "Accept": "application/vnd.github+json",
    }
    token = os.environ.get("GITHUB_TOKEN", "").strip()
    if token and base.startswith("https://api.github.com"):
        headers["Authorization"] = f"Bearer {token}"

    request = urllib.request.Request(url, headers=headers, method="GET")
    opener = urllib.request.build_opener(_NoRedirectHandler())
    try:
        with opener.open(request, timeout=float(timeout)) as response:
            http_status = getattr(response, "status", 200)
            raw = response.read(MAX_RESPONSE_BYTES + 1)
    except urllib.error.HTTPError as exc:
        retry_after = exc.headers.get("Retry-After") if exc.headers else None
        code = exc.code
        exc.close()
        if code in {301, 302, 303, 307, 308}:
            return _unresolved_record(slug, "redirect-blocked", http_status=code)
        if code == 404:
            return _unresolved_record(slug, "not-found", http_status=404)
        if code in {403, 429}:
            return _unresolved_record(
                slug,
                "rate-limited-or-forbidden",
                http_status=code,
                rate_limited=True,
                retry_after=retry_after,
            )
        return _unresolved_record(slug, f"http-error-{code}", http_status=code)
    except (urllib.error.URLError, TimeoutError, socket.timeout, OSError) as exc:
        return _unresolved_record(slug, f"network-or-timeout: {exc}")

    if len(raw) > MAX_RESPONSE_BYTES:
        return _unresolved_record(slug, "response-exceeds-1mb-limit", http_status=http_status)

    try:
        data = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return _unresolved_record(slug, "invalid-json", http_status=http_status)
    if not isinstance(data, dict) or not data.get("full_name"):
        return _unresolved_record(slug, "unexpected-payload", http_status=http_status)

    lic = data.get("license") or {}
    archived = bool(data.get("archived", False))
    record = {
        "schema_version": "1.0",
        "repo": data.get("full_name", slug),
        "html_url": data.get("html_url", f"https://github.com/{slug}"),
        "default_branch": data.get("default_branch"),
        "archived": archived,
        "pushed_at": data.get("pushed_at"),
        "stargazers_count": data.get("stargazers_count"),
        "language": data.get("language"),
        "topics": sorted(data.get("topics") or []),
        "license_hint": lic.get("spdx_id") if isinstance(lic, dict) else "unknown",
        "license_verified": False,
        "state": "metadata-only",
        "integration_recommendation": "archived-review-required" if archived else "reference-only",
        "cache_hit": False,
        "observed_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "security_warning": (
            "Read-only GitHub API metadata only; never treats license_hint as legal verification "
            "or executes upstream build/setup scripts."
        ),
    }
    if cache_dir is not None:
        _write_cache(Path(cache_dir), slug, record)
    return record


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True, help="GitHub repository slug in owner/repo format")
    parser.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT_SECONDS)
    parser.add_argument("--cache-dir", type=Path, default=None)
    parser.add_argument("--cache-ttl-seconds", type=int, default=3600)
    parser.add_argument("--format", choices=("json", "text"), default="json")
    args = parser.parse_args(argv)

    try:
        record = fetch_repo_metadata(
            args.repo,
            timeout=args.timeout,
            cache_dir=args.cache_dir,
            cache_ttl_seconds=args.cache_ttl_seconds,
        )
    except ValueError as exc:
        parser.exit(2, f"ERROR: {exc}\n")

    if args.format == "json":
        print(json.dumps(record, indent=2, ensure_ascii=False, sort_keys=True))
    else:
        print(f"Repo: {record['repo']} | state={record['state']} | archived={record.get('archived')}")
        print(f"  license_hint={record.get('license_hint')} (license_verified={record['license_verified']})")
        print(f"  recommendation={record['integration_recommendation']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
