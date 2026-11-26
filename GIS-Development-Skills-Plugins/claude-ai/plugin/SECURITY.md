# Security policy

## Scope

This repository distributes GIS-development Agent Skills, reference guides and testable GIS engineering examples; it is not a hosted security scanning or incident-response service.

## Reporting a vulnerability

Please do **not** publish exploitable details, live credentials, private location information or sensitive datasets in public GitHub issues. Prefer the repository's GitHub **Private vulnerability reporting** facility (Security > Advisories > Report a vulnerability) when enabled. If it is unavailable, contact the maintainer using the public contact route shown on the project page to request a confidential channel first; do not attach secrets to the first message.

Provide a minimal reproducible case with synthetic data, affected commit/file, risk and non-destructive reproduction steps. Do not access other users' data or attack live services while testing.

## Response and disclosure

Maintainers triage reports, reproduce in an isolated environment and fix/mitigate before public disclosure when feasible. No guaranteed response or patch-time SLA is claimed.

## Hardening commitments

- Treat external skills, MCP tools and geospatial files as untrusted until reviewed.
- No secrets in source code, sample fixtures, logging or acceptance evidence.
- No destruction of user GIS data without explicit authorization, backup and rollback.
- Use free/offline scanning first, and mark unavailable external scans as **not run**.
- Pin upstream actions and dependencies when integrating new CI/security tools.
- Record security evidence and limitations honestly.

See [GIS Security Guardian](skills/gis-security-guardian/SKILL.md) and [tooling guide](references/security/tooling-and-ci.md).
