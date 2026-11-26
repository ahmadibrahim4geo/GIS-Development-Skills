---
name: modern-web-guidance
description: Use GoogleChrome Modern Web Guidance with UI/UX Pro Max for creating, changing, or reviewing browser-based interfaces, standalone HTML, CSS, web components and frontend applications, including WebView interfaces and the frontend part of full-stack work. Verify both local providers before consulting them. Apply browser-compatible implementation guidance, accessible interaction patterns and fallbacks.
license: MIT
compatibility: Python 3.11+, Node.js 22+, reviewed Modern Web Guidance npm archive and a compatible UI/UX Pro Max installation with its local scripts and data. CI static checks need no external provider.
---

# Modern Web Guidance

For browser UI work, use the [paired workflow](../../references/modern-web-guidance-workflow.md) with UI/UX Pro Max even when the user simply asks for an HTML file. Keep the existing framework and design system on edits. Add [Geospatial Web Mapping](../geospatial-web-mapping/SKILL.md) for work on an actual map renderer.

1. Review provider provenance and permissions with [Security Guardian](../gis-security-guardian/SKILL.md). Use a working Python interpreter to run the paired readiness command in the workflow. If either provider fails, report the missing requirement and keep the paired route pending.
2. Before writing UI code, search Modern Web Guidance using a focused English capability query and retrieve matching guide IDs. Follow the browser support and fallback advice. Use UI/UX Pro Max to generate a design system for new pages, or run a focused UX lookup for an existing interface.
3. Implement the requested behavior and verify it in the target browser. Record the guide IDs and actual design decisions used. Include keyboard, focus, responsive layout, and RTL checks when they apply. Use [DoneProof](../completion-evidence/SKILL.md) for claims about execution.

Apply the [free-first policy](../../references/free-first-policy.md). The repository integration is MIT-licensed. The upstream tool and guides are available under Apache-2.0 and accompanying third-party notices. [Upstream release](https://github.com/GoogleChrome/modern-web-guidance/releases/tag/v1.0.1)
