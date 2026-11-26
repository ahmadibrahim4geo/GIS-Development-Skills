# Universal Agent Context Memory & Sessional Handoff Architecture

## 1. Executive Summary & Problem Statement

When an AI agent starts a fresh session, resumes after context compaction (`/compact`), or is handed off to a peer worker in a multi-agent swarm, it faces the **Cold-Start Problem**:
- Re-scanning directories and loading unrelated code increases the context needed to resume.
- Context window space is squandered before implementation even begins.
- Hallucinations increase as outdated conversational logs accumulate.

Based on `muratcankoylan/Agent-Skills-for-Context-Engineering`, this document establishes the **Modular `context/` Memory Standard** for all software projects, GIS tools, and skills developed in this repository.

---

## 2. The 5-File Modular `context/` Architecture

Every software project maintains a dedicated, lightweight `context/` directory in its project root:

```
project-root/
└── context/
    ├── PROJECT_MAP.md       <-- High-level system architecture, stack, invariants (<60 lines)
    ├── MODULE_INDEX.md      <-- Table of modules, classes, and ownership (<100 lines)
    ├── CURRENT_HANDOFF.md   <-- Active state: completed, in-progress, next step (<40 lines)
    ├── COMMAND_REGISTRY.md  <-- Canonical build, test, and lint commands (<30 lines)
    └── DEPENDENCY_MAP.md    <-- Inter-module and third-party dependency graph (<40 lines)
```

---

## 3. Specifications & File Templates

### 3.1 `PROJECT_MAP.md` (Architecture Snapshot)
```markdown
# Project Architectural Map
- **Project**: Urban Design Studio (UDS) / Universal Desktop CAD/GIS
- **Stack**: C++20, Qt 6.7 Widgets, QOpenGLWidget / Vulkan, GDAL/GEOS, earcut.hpp
- **Core Invariants**:
  1. Engineering Core is strictly decoupled from Rendering Viewport.
  2. All coordinates stored in 64-bit double precision with Camera-Relative Local Render Origin.
  3. Every AI Copilot action must be wrapped in QUndoCommand (Ctrl+Z reversibility).
  4. All AI tool payloads must pass strict C++ JSON Schema validation.
- **Root Paths**:
  - `src/core/`: Spatial data structures and relational DAG engine.
  - `src/gui/`: SARibbon, Qt-ADS docking workspace, and QtPropertyBrowser.
  - `src/sim/`: Solar, D8 hydrology, and SUMO traffic engines.
```

### 3.2 `CURRENT_HANDOFF.md` (Active Sessional State)
```markdown
# Current Sessional Handoff
- **Active Task**: UDS-004 Parametric Spatial Hierarchy & DAG Cascades
- **Status**: IN_PROGRESS (Road alignment complete; parcel setback solver active)
- **Latest Verified Milestone**:
  - `earcut.hpp` polygon triangulation verified on 180 demo features.
  - Test command: `python -m unittest tests/test_urban_design_competency.py` (ALL PASS)
- **Immediate Next Step**:
  - Implement Clipper2 parcel setback deflation logic in `src/core/SetbackSolver.cpp`.
- **Known Blockers / Caveats**: None.
```

### 3.3 `COMMAND_REGISTRY.md` (Verified Build & Test Commands)
```markdown
# Canonical Command Registry
- **Configure**: `cmake -B build -S . -DCMAKE_BUILD_TYPE=Release`
- **Build**: `cmake --build build --config Release -j 8`
- **Unit Tests**: `ctest --test-dir build --output-on-failure`
- **Python Harness**: `python -m unittest discover -s tests -v`
- **Security Audit**: `python scripts/security_audit.py --root .`
- **Plan Verification**: `python scripts/verify_completion.py doneproof-UDS.json --plan plan.json`
```

---

## 4. Checkpoint and resume

When an agent enters a project or begins a turn:
1. Read `context/CURRENT_HANDOFF.md` for the active task, approved revision, last relevant evidence and next action. Verify the journal and compare the handoff with the current project root and working state.
2. If the evidence or affected files changed, repeat the relevant narrow check before relying on the saved state. Open `context/PROJECT_MAP.md` or other references for remaining gaps.
3. Measure elapsed time or token usage against the same task and inputs when reporting an improvement. Label bytes or lines read as a proxy when token data is unavailable.

---

## 5. Maintenance Protocol
- The active developer or agent **must update `CURRENT_HANDOFF.md`** upon completing any task milestone.
- Outdated handoff notes are overwritten; historical logs are archived in permanent journals (`.agent-development-log/`) rather than cluttering active context.
