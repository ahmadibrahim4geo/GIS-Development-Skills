# Portable execution guidance

Use this reference to choose effort, capabilities and a debugging approach. The [repository-wide contract](repository-wide-skill-orchestration.md) owns workflow states, approval and responsibilities. These modes are host-selected guidance, not new compiler fields or automatically enforced gates.

## Model and agent independence

The guidance does not require a named model vendor or agent framework. The host must read the relevant instructions, interpret the request and perform authorized actions. Installation, tool access and behavior require verification in each named client/version; Markdown does not establish universal compatibility.

Describe required capabilities first: read project files, search sources, execute a check, inspect a UI or persist evidence. Discover which authorized host tools provide them. A shell, browser, connector or particular CLI is an implementation choice. An equivalent capability must preserve the outcome, permissions and evidence level. Otherwise report the affected operation as BLOCKED or NOT RUN and continue independent permitted work.

## Choose proportionate effort

State the mode briefly when it explains the approach; a factual answer need not announce internal process.

| Mode | Appropriate scope | Record and verification |
| --- | --- | --- |
| Lite | A clear read-only explanation or one small reversible change | Check the relevant fact or changed artifact. Existing approval rules still apply to changes. A simple answer may carry evidence in the reply. |
| Standard | Several related steps in one area | Retain reviewed criteria and the next action in the existing plan/journal; verify meaningful outcomes and relevant regressions. |
| Deep | Cross-component, uncertain, sensitive or release work | Resolve risky unknowns first; retain dependencies, decisions, rollback points and per-criterion evidence, including required native checks. |

Scale the amount of planning and checking, never the truth of a claim. Modes do not waive review, source protection, licensing or host permissions. Material changes to goals or effects follow the existing plan-revision gate; a mode choice alone grants no scope. [Intent Orchestrator](../skills/prompt-intent-orchestrator/SKILL.md) owns review and [Security Guardian](../skills/gis-security-guardian/SKILL.md) owns safety preflight.

## Work within existing ownership

1. **Understand and inspect:** recover the user's outcome, constraints, protected data and success criteria. Read the affected project and existing implementation before choosing changes.
2. **Choose reuse or construction:** inspect local utilities and accepted dependencies first. For unresolved needs use [GIS Code Discovery](../skills/gis-code-discovery/SKILL.md) to evaluate official sources or external candidates. Record fit, version, license and the decision. GitHub is one possible source; external search is conditional on the gap. Unclear licensing permits conceptual study only, without copying source text or code.
3. **Execute a verifiable slice:** follow the approved dependency order through the [GIS router](../skills/gis-development/SKILL.md). Prefer a small end-to-end result before expansion. Recheck files against their read baseline before overwriting, preserve unrelated edits and inspect the written result.
4. **Check and diagnose:** use the specialist's acceptance checks. Capture input, versions, actual error and expected result; test one causal hypothesis with a small probe, then rerun the failed check after correction. Compare the same measurement before and after when claiming improvement.
5. **Record and hand off:** retain decisions, the next action and evidence in the existing [Development Journal](../skills/agent-development-journal/SKILL.md), reviewed plan and acceptance report. Do not introduce a competing diary or status vocabulary. [DoneProof](../skills/completion-evidence/SKILL.md) owns completion claims.

These practices fit inside the canonical workflow. Before resuming, verify the journal and compare it with current files and observed checks; historical reports cannot authorize new actions.

## Bound diagnosis and optional delegation

Do not repeat a failing action with unchanged inputs and no new evidence. After repeated failure of a hypothesis, inspect assumptions or reduce the case before another change. Bound retries by cost, side effects and authorized scope; failure does not authorize a new engine, installation, deletion or deployment. If progress needs missing input, capability or permission, report that dependency and preserve independent progress. Avoid abandoning solvable work after a universal fixed attempt count.

Parallel agents are optional and require host support plus authorization from the user or applicable host/project instructions. Give independent scopes and complete briefs, keep file ownership separate and reconcile returned evidence. Sequential execution must remain supported.

## Match verification to the claim

For explanations, check supplied material or relevant sources. For documentation, compare the brief with the written result and inspect links. For code, use relevant execution and regression checks. For UI, inspect requested behavior in the actual supported host when available. Particular tools, such as browser drivers or 3D editors, belong to the relevant specialist and task.

Fixtures, mocks, source reviews and screenshots cannot replace required native integration or packaged workflows. Retain T0–T4 meanings from the [evidence registry](evidence-tiers.json) and [quality benchmark](../docs/QUALITY_BENCHMARK.md). Record actual commands/actions, observations and gaps. Static checks prove those checks only, not model compliance or correct installation in every client.

## ملخص الاستخدام بالعربية

المنهج مستقل عن اسم النموذج وإطار الوكيل، والتنفيذ يعتمد على قدرات البيئة وصلاحياتها الفعلية. ملف Markdown لا يثبت التوافق مع كل البرامج أو يضمن التزام النماذج به.

- **Lite — خفيف:** سؤال واضح أو تعديل صغير قابل للتراجع، مع تحقق مناسب من المعلومة أو الناتج.
- **Standard — اعتيادي:** خطوات مترابطة، مع خطة ومعايير قبول وقرار تالٍ محفوظة في السجل الحالي.
- **Deep — موسع:** عمل معقد أو حساس أو إصدار، مع ترتيب التبعيات والمخاطر وأدلة لكل نتيجة.

المستوى لا يُسقط موافقة المستخدم أو حدود الصلاحيات. افحص الموجود قبل البحث الخارجي أو البناء، وسجّل سبب الاختيار والترخيص. اختبر فرضية محددة عند الخطأ وأعد نفس الفحص بعد الإصلاح؛ تجنب التكرار دون دليل جديد. استخدم الوكلاء الفرعيين عند توفر الدعم والتصريح فقط، مع بقاء التنفيذ المتسلسل ممكنًا.

يظل منسق النية مسؤولًا عن فهم الطلب ومراجعته، وموجّه GIS عن اختيار المختص، وحارس الأمان عن حدود التنفيذ، وسجل التطوير عن التاريخ، وDoneProof عن ربط الادعاء بالدليل. غياب برنامج GIS أو أداة لازمة يترك الاختبار المعني NOT RUN أو BLOCKED؛ الاختبار البديل لا يثبت تشغيلًا أصليًا لم يحدث.
