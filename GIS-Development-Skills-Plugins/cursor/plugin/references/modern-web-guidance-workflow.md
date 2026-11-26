# Modern Web Guidance and UI/UX Pro Max

Use both providers for new or changed HTML, web interfaces, WebView frontends and the frontend portion of full-stack requests. The [GIS interface skill](../skills/gis-ui-ux-design-testing/SKILL.md) owns usability and acceptance. The [Modern Web Guidance skill](../skills/modern-web-guidance/SKILL.md) coordinates local search and retrieval. Server-only, native desktop UI and text-only edits stay with their existing routes.

## Setup and readiness

1. Use a working Python 3.11 or later and Node.js 22 or later. Check the interpreter actually selected by the host. On Windows a Store alias may be present on PATH without a working runtime. Use the installed interpreter's absolute path if needed.
2. After authorizing the public download, place the official npm archive at `testing results/web-guidance/modern-web-guidance-1.0.1.tgz` in the target project, or pass `--package` with a reviewed local path. The helper verifies the archive size and SHA-512 before extraction or execution. It uses the included CLI, guides and search index directly. Preserve the artifact's `LICENSE` and `THIRD_PARTY_NOTICES`. [Registry archive](https://registry.npmjs.org/modern-web-guidance/-/modern-web-guidance-1.0.1.tgz) · [Release source](https://github.com/GoogleChrome/modern-web-guidance/tree/64a6d708f5a43f2cd3fde5d4d7db3905ba1bdf65)
3. Use the host-reviewed UI/UX Pro Max installation with its `SKILL.md`, Python helpers, CSV data and generated search references. The helper looks in the project `.agents/skills` and `.claude/skills`, then the corresponding user skill directories and `.codex/skills`. Pass `--ui-ux-dir` for a different approved installation. Review the exact local scripts and assets before authorizing their execution, especially if the installed build differs from its public source. [Upstream source and installer](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) · [MIT license](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/blob/6ec2bb58334ca3014573c4cbd4834ee3a40afd9d/LICENSE)
4. Run the helper from the target project's root. Adjust the path to `scripts/web_guidance.py` when your suite is installed elsewhere. The `check` command requires a real Modern Web Guidance search and guide result, plus UX results and a design system from UI/UX Pro Max. Continue the paired route when it reports `READY`.

```sh
python -B scripts/web_guidance.py check
python -B scripts/web_guidance.py search "confirmation modal dialog"
python -B scripts/web_guidance.py retrieve "dialog"
python -B scripts/web_guidance.py design "responsive Arabic dashboard with confirmation"
python -B scripts/web_guidance.py ux "keyboard focus dialog accessibility"
```

The helper disables upstream telemetry and file logging for its child processes. It exposes search and retrieve for the reviewed web package and non-persisting UX and design queries for the installed design skill. Send generic capability queries without project names or private data. Project browser policies and permissions still apply. Re-run readiness when paths, files or runtime versions change.

## Apply and verify

Load only guides related to the task and use the pinned helper to follow any guide cross-references. Use short English capability queries with either provider and implement the interface in the user's requested language. Use Modern Web Guidance for web semantics, browser support and fallbacks. Use UI/UX Pro Max for layout, hierarchy, visual states, responsiveness and interaction. Preserve the existing design system on edits. Run the visible action in the target browser and verify relevant keyboard, focus, RTL and narrow-screen behavior. Capture the matched guide IDs, design output and observed browser behavior independently.

Upgrade by reviewing the new upstream release, notices, archive digest and command behavior, then rerun the same readiness and browser checks. Keep the previous reviewed archive available for rollback.
