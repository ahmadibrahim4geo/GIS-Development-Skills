# Natural-language intent → GIS task plan (offline example)

Original request: "عايز أصلح تشغيل الشبكة الإحداثية وتسميات خطوط الطول ودوائر العرض والمبالغة الرأسية في برنامج ZEarth."

The three-task [example-plan.json](example-plan.json) demonstrates separating grid controls from terrain exaggeration and a dependent verification step. It is **DRAFT / NOT AUTHORIZED**. It does not modify ZEarth, call a language model or certify working controls.

From the repository root:

~~~bash
python scripts/intent_router.py --text "عايز أصلح الشبكة والـTerrain في ZEarth" --format json
python scripts/intent_router.py --plan examples/intent-orchestrator/example-plan.json
python scripts/intent_router.py --plan examples/intent-orchestrator/example-plan.json --workflow --format json
python scripts/intent_router.py --plan examples/intent-orchestrator/example-plan.json --gate
python -m unittest tests.test_intent_orchestrator -v
~~~

Expected: the first returns only **conservative lexical hints** with no inferred goal. The second checks the reviewed plan; the workflow preview **compiles the explicit user goal, outcomes and ordered task dependencies** but cannot execute them; the final gated command exits nonzero because the example is unapproved. A host agent must obtain real permission, verify tools, use actual domain specialists and log GIS evidence independently.
