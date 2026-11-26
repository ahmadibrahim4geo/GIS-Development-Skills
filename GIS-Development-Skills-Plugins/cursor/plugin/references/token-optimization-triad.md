# Universal Token Optimization Triad for Software & Geoprocessing Agents

## 1. Executive Summary & Purpose

This document formalizes the **Token Optimization Triad** as a universal operational standard for all autonomous AI agents, developers, and code copilots working within the `GIS Development Skills` hub.

In large-scale desktop software and geoprocessing tool development, context window exhaustion, latency spikes, and hallucinations are directly caused by three anti-patterns:
1. **Context Over-Reading**: Loading entire multi-thousand-line repositories or large datasets into the context window prior to scoping.
2. **Whole-File Rewriting**: Overwriting 500-line source files to modify a single 3-line function.
3. **Verbose Log Dumping**: Letting unbuffered terminal commands dump megabytes of compiler output or test progress into agent memory.

The **Token Optimization Triad** solves these issues through a structured, three-phase engineering discipline:

```
[Phase 1: Ponytail] ──────> [Phase 2: Caveman] ──────> [Phase 3: Token Optimizer]
Pre-Coding Scoping           In-Flight Surgical Edits   Post-Coding Compaction
(Targeted reads & anchors)   (Diff patches & quiet CLI) (Session cleanup & handoffs)
```

---

## 2. Phase 1: Pre-Coding Scope Reduction (`Ponytail` Standard)

Based on `DietrichGebert/ponytail`:

### 2.1 Principles
- **Anchor Before Reading**: Never read an entire source file blindly. Use targeted symbol discovery (`grep`, AST indexers, symbol outlines) to locate exact line ranges.
- **Targeted reads**: Start with the relevant symbols and callers. Expand to the full file or dependency when contracts, invariants or review require it.
- **Scoped edits**: Identify the affected files and interfaces. Preserve unrelated changes and follow the reviewed scope if the work needs more files.

### 2.2 Operational Anti-Pattern vs. Best Practice
- **Bad**: Reading all 800 lines of `SpatialDocument.cpp` to understand a single coordinate transformation method.
- **Example**: Locate `applyLocalOriginShift`, inspect its body and callers, and expand the read if coordinate-system assumptions remain unclear.

---

## 3. Phase 2: In-Flight Surgical Patching (`Caveman` Standard)

Based on `JuliusBrussee/caveman`:

### 3.1 The "Least Complete Change" Principle
- **Surgical Edits Only**: Edits must be executed via localized text replacement tools (`edit_file`) replacing only the target lines. Never replace an entire 600-line file with a newly generated copy.
- **Compact Git Diffs**: Code changes should produce clean, minimal git diffs that can be reviewed in seconds by human engineers.

### 3.2 Quiet Execution Discipline
- **Silence Compiler Noise**: When invoking compilers (`cmake --build`, `ninja`, `cargo`, `vcpkg`), pass quiet flags or pipe output through summary filters.
- **Test Summary Only**: Unit test runners must output total counts and failed test traces only (e.g. `pytest -q` or `ctest --output-on-failure`). Never dump thousands of lines of passing test names into the conversation.

---

## 4. Phase 3: Post-Coding Compaction (`Token Optimizer` Standard)

Based on `alexgreensh/token-optimizer`:

### 4.1 Artifact & Scratch Compaction
- **Evidence retention**: Keep relevant test output and readback in their existing evidence locations. Summarize the essentials in conversation.
- **Checkpoint distillation**: Preserve the active task, verified result, next action and any open dependency in the existing handoff for substantial work.

### 4.2 Legal & Licensing Quarantine Notice
> **Important Legal Boundary**: `alexgreensh/token-optimizer` is licensed under `PolyForm-Noncommercial-1.0`. In accordance with our repository security standards, its scripts and techniques are quarantined strictly to developer-side agent workflows. They are **never packaged, bundled, or distributed** inside shipped desktop software binaries.

---

## 5. Universal Operational Rules Checklist

Every agent operating in this repository must adhere to this checklist before, during, and after code edits:

| Phase | Checkpoint Rule | Verification Mechanism |
| :--- | :--- | :--- |
| **Pre-Coding** | Are reads scoped to the task? | Relevant definitions and callers found and surrounding contracts inspected as needed. |
| **Pre-Coding** | Is the change scope isolated? | Explicit list of modified files declared upfront. |
| **During Coding** | Is the edit surgical? | `edit_file` used with tight match blocks; no whole-file overwrites. |
| **During Coding** | Are commands quiet? | Test and build flags use quiet/terse modes. |
| **Post-Coding** | Is decisive evidence accessible? | Handoff links to the relevant logs or readback outside the active context. |
| **Post-Coding** | Is handoff recorded? | Sessional progress distilled into `context/CURRENT_HANDOFF.md`. |
