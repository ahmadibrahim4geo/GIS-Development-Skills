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

1. **Understand:** identify the user's outcome, limits, protected inputs and a result that can be checked.
2. **Inspect:** read the affected files, callers or inputs. For a reported failure, reproduce it with the smallest representative input and record expected versus actual behavior. Identify the earliest point where the behavior differs.
3. **Decide:** inspect existing utilities and compatible installed dependencies. If a material gap remains, use official sources and [GIS Code Discovery](../skills/gis-code-discovery/SKILL.md). Record consequential reuse, dependency or architecture choices with the evidence that supports them. Evaluate source and license before reuse.
4. **Split and execute:** follow the approved dependency order through the [GIS router](../skills/gis-development/SKILL.md). Resolve the uncertainty most likely to change the approach early. Deliver a narrow end-to-end result before expansion. Recheck the baseline before overwriting and read back the changed artifact.
5. **Test:** first run the focused check, then the relevant regression or acceptance checks. Include a representative failure path when the task warrants it. Match the test to the user's deliverable and record the outcome actually observed.
6. **Fix and recheck:** when a check fails, state one causal hypothesis and test it with a small, discriminating probe. Change the hypothesis when the result contradicts it. Rerun the original reproduction and relevant checks after a correction. Preserve the decision, evidence and next action in the existing [journal](../skills/agent-development-journal/SKILL.md), plan and [DoneProof](../skills/completion-evidence/SKILL.md) report.

Scale these steps to the task. On resumption, compare the current root, revision and working state with the saved handoff and verify its latest relevant claim. Continue from the first unverified or stale step. Keep the task, evidence and next action in the existing handoff.

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
