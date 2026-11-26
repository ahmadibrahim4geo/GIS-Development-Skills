"""Exercise the browser-only Project Wizard's real JS handlers in a Node DOM stub.

No network, package manager or paid browser services are required. This checks
generating a plan, bilingual switching, dirty-state invalidation and download.
"""
import importlib.util
import json
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

HARNESS = r"""
'use strict';
const assert = require('node:assert/strict');
const vm = require('node:vm');
const fs = require('node:fs');
const code = fs.readFileSync(process.argv[2], 'utf8');
const selectors = {
  type: ['desktop','mobile','pro','arcmap','dual','qgis','qgis-engine','web','remote','database','geoai'],
  architectureChange:['none','ui-reorganization','ui-shell-migration','engine-integration','engine-replacement'],
  locale: ['ar-en','en','multi'], files:['yes','no'], license:['free','host'], qualityFocus:['standard','audit','e2e','flow','ux','all'], deviceNeeds:['none','time','location','hardware','all'], mobilePlatform:['android','ios','both'], mobileNetwork:['local','offline-sync','online'], mobileSignIn:['guest','optional','required']
};
const elements = Object.create(null);
function node(id) {
  return elements[id] ||= {
    id, value:'', textContent:'', placeholder:'', disabled:false,
    listeners:{}, options:[], onclick:null,
    addEventListener(type, fn){this.listeners[type]=fn},
    click(){this.clicked=true},
    fire(type){assert.equal(typeof this.listeners[type], 'function');this.listeners[type]()}
  };
}
for(const [id, values] of Object.entries(selectors)){
  node(id).options = values.map(value=>({value,textContent:value}));
  node(id).value=values[0];
}
for (const id of ['lang','heading','intro','typeLabel','localeLabel','filesLabel',
  'licenseLabel','qualityLabel','deviceLabel','mobileSettings','mobilePlatformLabel','mobileNetworkLabel','mobileSignInLabel','jsonHint','detailsLabel','details','goalLabel','goal','successLabel','success','generate','download','downloadJson','resultLabel','result','status',
  'homeLink','roadmapLink','kmlLink','reliabilityLink','workflowLink','wizardPrivacy',
  'architectureLabel','architectureHint','architectureSettings','architectureSourceLabel','architectureSource','architectureUiLabel','architectureUi','architectureLink']) node(id);
node('download').disabled = true;
node('downloadJson').disabled = true;
let lastLink=null, lastBlob=null, revoke=null;
const document = {
  documentElement:{lang:'en',dir:'ltr'},
  getElementById:id=>elements[id]||null,
  createElement:tag=>{
    assert.equal(tag,'a');
    lastLink={href:'',download:'',click(){this.clicked=true}};
    return lastLink;
  }
};
class Blob {
  constructor(parts,opts){lastBlob={parts,type:opts.type};}
}
const URL={
  createObjectURL:()=> 'blob:plan',
  revokeObjectURL:url=>{revoke=url}
};
vm.runInNewContext(code,{document,Blob,URL,setTimeout:fn=>fn()});
const e=id=>elements[id];
assert.equal(document.documentElement.lang,'en');
assert.equal(e('download').disabled,true);
assert.equal(e('downloadJson').disabled,true);
assert.equal(e('architectureSettings').hidden,true);
e('details').value='Preserve icons, folders and styles.';
e('goal').value='Reliable KMZ import without losing custom icons.';
e('success').value='Round-trip styles and folders are identical.';
e('generate').onclick();
assert.equal(e('download').disabled,false);
assert.equal(e('downloadJson').disabled,false);
assert.match(e('result').textContent,/GIS Project Implementation Plan/);
assert.match(e('result').textContent,/KML\/KMZ/);
assert.match(e('result').textContent,/Preserve icons/);
assert.match(e('result').textContent,/Reliable KMZ import/);
assert.match(e('result').textContent,/Round-trip styles/);
assert.match(e('result').textContent,/skills\/prompt-intent-orchestrator\/SKILL\.md/);
assert.match(e('result').textContent,/repository-wide-skill-orchestration.md/);
e('download').onclick();
assert.equal(lastLink.download,'gis-project-plan-en.md');
assert.equal(lastLink.clicked,true);
assert.match(lastBlob.parts[0],/Project Implementation Plan/);
assert.equal(revoke,'blob:plan');
e('downloadJson').onclick();
assert.equal(lastLink.download,'gis-workflow-draft.json');
assert.equal(lastBlob.type,'application/json;charset=utf-8');
const firstJSON=JSON.parse(lastBlob.parts[0]);
assert.equal(firstJSON.status,'draft');
assert.equal(firstJSON.approval.approved_by_user,false);
assert.equal(firstJSON.goal,'Reliable KMZ import without losing custom icons.');
assert.equal(firstJSON.success_criteria[0],'Round-trip styles and folders are identical.');
assert.equal(firstJSON.tasks.length,3);
assert.equal(firstJSON.tasks[0].owner_skill,'gis-desktop-application-development');
assert.deepEqual(firstJSON.tasks[2].depends_on,['T2']);
assert.ok(firstJSON.tasks.every(task=>!('architecture' in task)));
console.log('STRUCTURED_WIZARD:'+JSON.stringify(firstJSON));
assert.ok(!e('result').textContent.includes('skills/gis-ui-command-audit/SKILL.md'));
e('qualityFocus').value='all';
e('qualityFocus').fire('change');
assert.equal(e('downloadJson').disabled,true);
e('generate').onclick();
const qualityList=['gis-ui-command-audit','gis-desktop-e2e-testing','gis-data-flow-diagnostics','gis-ui-ux-design-testing'];
for (const slug of qualityList) {
  assert.ok(e('result').textContent.includes('skills/'+slug+'/SKILL.md'));
}
e('downloadJson').onclick();
const qaPlan=JSON.parse(lastBlob.parts[0]);
for (const slug of qualityList) {
  assert.ok(qaPlan.tasks[1].skills.includes(slug));
}
assert.equal(qaPlan.status,'draft');
console.log('QUALITY_WIZARD:'+JSON.stringify(qaPlan));
e('deviceNeeds').value='location';
e('deviceNeeds').fire('change');
assert.equal(e('downloadJson').disabled,true);
e('generate').onclick();
assert.match(e('result').textContent,/OS\/device capability and permission scope/);
e('downloadJson').onclick();
const devicePlan=JSON.parse(lastBlob.parts[0]);
assert.ok(devicePlan.tasks[1].skills.includes('system-capabilities-and-permissions'));
assert.ok(devicePlan.tasks[1].skills.includes('gis-device-context'));
e('deviceNeeds').value='none';
e('deviceNeeds').fire('change');
e('qualityFocus').value='standard';
e('qualityFocus').fire('change');
assert.equal(e('downloadJson').disabled,true);
e('generate').onclick();
e('goal').value='Different expected outcome';
e('goal').fire('input');
assert.equal(e('download').disabled,true);
assert.equal(e('downloadJson').disabled,true);
e('generate').onclick();
assert.match(e('result').textContent,/Different expected outcome/);
e('success').value='Observed real-output check';
e('success').fire('input');
assert.equal(e('download').disabled,true);
assert.equal(e('downloadJson').disabled,true);
e('generate').onclick();
assert.match(e('result').textContent,/Observed real-output check/);
e('type').value='qgis';
e('type').fire('change');
assert.equal(e('download').disabled,true);
assert.equal(e('result').textContent,'');
e('generate').onclick();
assert.match(e('result').textContent,/PyQGIS/);
assert.match(e('result').textContent,/skills\/qgis-plugin-development\/SKILL.md/);
e('type').value='mobile';e('type').fire('change');
assert.equal(e('mobileSettings').hidden,false);
assert.match(e('qualityFocus').options.find(x=>x.value==='e2e').textContent,/Android\/iOS/);
e('mobilePlatform').value='both';e('mobilePlatform').fire('change');
e('mobileNetwork').value='offline-sync';e('mobileNetwork').fire('change');
e('mobileSignIn').value='required';e('mobileSignIn').fire('change');
e('qualityFocus').value='e2e';e('qualityFocus').fire('change');
e('generate').onclick();
assert.match(e('result').textContent,/Mobile GIS implementation and native testing/);
assert.match(e('result').textContent,/Android \+ iOS/);
assert.match(e('result').textContent,/mobile-gis-offline-sync.md/);
e('downloadJson').onclick();
const mobilePlan=JSON.parse(lastBlob.parts[0]);
assert.equal(mobilePlan.tasks[1].owner_skill,'gis-mobile-application-development');
assert.ok(mobilePlan.tasks[1].skills.includes('system-capabilities-and-permissions'));
assert.ok(mobilePlan.tasks[1].skills.includes('gis-device-context'));
assert.ok(!mobilePlan.tasks[1].skills.includes('gis-desktop-e2e-testing'));
assert.ok(mobilePlan.constraints.some(x=>x.includes('Android + iOS')));
console.log('MOBILE_WIZARD:'+JSON.stringify(mobilePlan));
e('qualityFocus').value='standard';e('qualityFocus').fire('change');
e('type').value='qgis';e('type').fire('change');e('generate').onclick();
e('lang').onclick();
assert.equal(document.documentElement.lang,'ar');
assert.equal(document.documentElement.dir,'rtl');
assert.match(e('type').options[0].textContent,/تطبيق/);
assert.match(e('result').textContent,/خطة تنفيذ مشروع/);
assert.match(e('result').textContent,/إضافة QGIS/);
e('type').value='qgis-engine';
e('type').fire('change');
e('generate').onclick();
assert.match(e('result').textContent,/محرك QGIS لتطبيق مستقل/);
assert.match(e('result').textContent,/skills\/qgis-engine-integration\/SKILL.md/);
assert.match(e('result').textContent,/references\/qgis-engine-integration.md/);
e('lang').onclick();
assert.match(e('result').textContent,/QGIS Engine \/ Standalone GIS/);
e('lang').onclick();
assert.match(e('status').textContent,/تم إنشاء/);
e('download').onclick();
assert.equal(lastLink.download,'gis-project-plan-ar.md');
assert.match(lastBlob.parts[0],/متطلبات المستخدم/);
e('locale').value='en';
e('locale').fire('change');
assert.equal(e('download').disabled,true);
e('license').value='host';
e('files').value='no';
e('details').value='<img src=x onerror=alert(1)>';
e('details').fire('input');
e('generate').onclick();
assert.match(e('result').textContent,/التراخيص/);
assert.match(e('result').textContent,/<img src=x onerror=alert\(1\)>/);
assert.doesNotMatch(e('result').textContent,/skills\/gis-internationalization-arabic\/SKILL.md/);
assert.match(e('result').textContent,/دعم KML\/KMZ غير مطلوب/);
e('lang').onclick();
assert.equal(document.documentElement.lang,'en');
assert.match(e('result').textContent,/Commercial host allowed/);

// Free text alone never selects a delivery model or an architecture change.
e('type').value='qgis';e('type').fire('change');
e('details').value='حوّل أدوات QGIS إلى Ribbon باستخدام UI.js';e('details').fire('input');
e('goal').value='Preserve existing QGIS commands in the new interface';
e('success').value='Each migrated command keeps its handler and enabled state';
e('generate').onclick();e('downloadJson').onclick();
const unchangedPlan=JSON.parse(lastBlob.parts[0]);
assert.equal(unchangedPlan.tasks[1].owner_skill,'qgis-plugin-development');
assert.ok(!('architecture' in unchangedPlan.tasks[1]));
assert.ok(!unchangedPlan.tasks[1].skills.includes('gis-ui-command-audit'));

e('architectureChange').value='ui-reorganization';e('architectureChange').fire('change');
assert.equal(e('architectureSettings').hidden,false);
assert.equal(e('downloadJson').disabled,true);
assert.equal(e('download').disabled,true);
e('generate').onclick();e('downloadJson').onclick();
const unknownArchitecture=JSON.parse(lastBlob.parts[0]);
assert.equal(unknownArchitecture.tasks[1].architecture.source_host,'unresolved');
assert.equal(unknownArchitecture.tasks[1].architecture.ui_framework.name,'unresolved');
assert.equal(unknownArchitecture.tasks[1].architecture.target_host,'QGIS Plugin');

e('architectureSource').value='Existing QGIS plugin';e('architectureSource').fire('input');
assert.equal(e('downloadJson').disabled,true);
assert.equal(e('result').textContent,'');
e('generate').onclick();
e('architectureUi').value='UI.js';e('architectureUi').fire('input');
assert.equal(e('download').disabled,true);
assert.equal(e('downloadJson').disabled,true);
e('generate').onclick();
assert.match(e('result').textContent,/Architecture change \(draft\)/);
assert.match(e('result').textContent,/Existing host: Existing QGIS plugin/);
assert.match(e('result').textContent,/Requested UI component: UI.js/);
assert.match(e('result').textContent,/references\/ui-engine-architecture-contract.md/);
assert.match(e('architectureHint').textContent,/never installs or replaces/);

e('lang').onclick();
assert.equal(document.documentElement.lang,'ar');
assert.equal(document.documentElement.dir,'rtl');
assert.match(e('architectureLabel').textContent,/ما التغيير المطلوب/);
assert.match(e('architectureChange').options.find(x=>x.value==='ui-reorganization').textContent,/إعادة تنظيم/);
assert.match(e('architectureSource').placeholder,/إضافة QGIS/);
assert.match(e('architectureUi').placeholder,/اتركه فارغًا/);
assert.match(e('architectureHint').textContent,/لا يثبّت/);
assert.match(e('result').textContent,/التغيير المعماري \(مسودة\)/);
assert.match(e('result').textContent,/بيئة التسليم المختارة: إضافة QGIS/);
assert.equal(e('architectureSource').value,'Existing QGIS plugin');
assert.equal(e('architectureUi').value,'UI.js');
e('downloadJson').onclick();
const ribbonPlan=JSON.parse(lastBlob.parts[0]);
assert.equal(ribbonPlan.language,'ar');
assert.equal(ribbonPlan.tasks[1].owner_skill,'qgis-plugin-development');
assert.ok(!('architecture' in ribbonPlan.tasks[0]));
assert.ok(ribbonPlan.tasks[0].acceptance_criteria.some(x=>x.includes('source/target compatibility')));
const architecture=ribbonPlan.tasks[1].architecture;
assert.equal(architecture.source_host,'Existing QGIS plugin');
assert.equal(architecture.target_host,'QGIS Plugin');
assert.equal(architecture.ui_framework.name,'UI.js');
for(const component of ['ui_framework','renderer','gis_engine']){
  assert.equal(architecture[component].status,'unresolved');
  assert.equal(architecture[component].source_ref,null);
  assert.equal(architecture[component].version,null);
}
assert.equal(architecture.integration_mode,'unresolved');
assert.equal(architecture.command_inventory_ref,null);
assert.equal(architecture.flow_spec_ref,null);
assert.ok(ribbonPlan.constraints.some(x=>x.includes('Existing QGIS plugin')&&x.includes('UI.js')));
assert.equal(ribbonPlan.approval.approved_by_user,false);
assert.ok(!ribbonPlan.tasks[1].skills.includes('gis-desktop-application-development'));
assert.ok(!ribbonPlan.tasks[1].skills.includes('qgis-engine-integration'));
assert.ok(!ribbonPlan.tasks[1].skills.includes('geospatial-web-mapping'));
console.log('ARCHITECTURE_WIZARD:'+JSON.stringify(ribbonPlan));

const architectureCases=[];
for(const change of ['ui-reorganization','ui-shell-migration','engine-integration','engine-replacement']){
  e('architectureChange').value=change;e('architectureChange').fire('change');
  assert.equal(e('downloadJson').disabled,true);
  e('generate').onclick();e('downloadJson').onclick();
  const plan=JSON.parse(lastBlob.parts[0]);
  assert.equal(plan.tasks[1].owner_skill,'qgis-plugin-development');
  assert.equal(plan.tasks[1].architecture.change_type,change);
  const migration=change.startsWith('ui-');
  assert.equal(plan.tasks[1].skills.includes('gis-ui-command-audit'),migration);
  assert.equal(plan.tasks[1].skills.includes('gis-ui-ux-design-testing'),migration);
  assert.equal(plan.tasks[1].skills.includes('gis-data-flow-diagnostics'),!migration);
  assert.ok(!plan.tasks[1].skills.includes('gis-desktop-e2e-testing'));
  architectureCases.push(plan);
}
architectureCases.push(unknownArchitecture);
console.log('ARCHITECTURE_CASES:'+JSON.stringify(architectureCases));
e('lang').onclick();
assert.match(e('architectureLabel').textContent,/What changes/);
assert.match(e('architectureChange').options.find(x=>x.value==='engine-integration').textContent,/Connect a GIS engine/);
assert.match(e('architectureLink').textContent,/UI and engine planning/);
e('architectureChange').value='none';e('architectureChange').fire('change');
assert.equal(e('architectureSettings').hidden,true);
e('generate').onclick();e('downloadJson').onclick();
const plainPlan=JSON.parse(lastBlob.parts[0]);
assert.ok(plainPlan.tasks.every(task=>!('architecture' in task)));
assert.ok(!plainPlan.tasks[1].skills.includes('gis-ui-command-audit'));
assert.ok(!plainPlan.tasks[1].skills.includes('gis-data-flow-diagnostics'));
assert.ok(!plainPlan.tasks[1].skills.includes('gis-ui-ux-design-testing'));
assert.equal(plainPlan.tasks[1].owner_skill,'qgis-plugin-development');
console.log('Wizard interaction contract passed: both languages, invalidation, selection and download.');
"""


class WizardBehaviorTests(unittest.TestCase):
    def test_wizard_behavior_in_node(self):
        node = shutil.which("node")
        if not node:
            self.skipTest("Node not installed; CI Node gate will test syntax")
        html = (ROOT / "project-wizard.html").read_text(encoding="utf-8")
        blocks = re.findall(r"<script>(.*?)</script>", html, re.S)
        self.assertEqual(len(blocks), 1)
        with tempfile.TemporaryDirectory() as tmp:
            script = Path(tmp) / "wizard.js"
            harness = Path(tmp) / "harness.cjs"
            script.write_text(blocks[0], encoding="utf-8")
            harness.write_text(HARNESS, encoding="utf-8")
            test = subprocess.run([node, str(harness), str(script)],
                                  capture_output=True, text=True, timeout=20)
            self.assertEqual(test.returncode, 0,
                             test.stdout + "\n" + test.stderr)
            structured = [line.split('STRUCTURED_WIZARD:', 1)[1]
                          for line in test.stdout.splitlines()
                          if line.startswith('STRUCTURED_WIZARD:')]
            self.assertEqual(len(structured), 1, test.stdout)
            blueprint = json.loads(structured[0])
            source = ROOT / 'scripts' / 'intent_router.py'
            spec = importlib.util.spec_from_file_location('wizard_intent_router', source)
            validator = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(validator)
            self.assertEqual([], validator.validate_plan(blueprint))
            compiled = validator.compile_workflow(blueprint)
            self.assertTrue(compiled['valid'], compiled['errors'])
            self.assertEqual('AWAITING_REVIEW', compiled['status'])
            self.assertFalse(compiled['can_execute'])
            self.assertEqual(['T1', 'T2', 'T3'], [t['task_id'] for t in compiled['steps']])
            qa_structured = [line.split('QUALITY_WIZARD:', 1)[1]
                             for line in test.stdout.splitlines()
                             if line.startswith('QUALITY_WIZARD:')]
            self.assertEqual(1, len(qa_structured), test.stdout)
            qa = json.loads(qa_structured[0])
            qa_compiled = validator.compile_workflow(qa)
            self.assertTrue(qa_compiled['valid'], qa_compiled['errors'])
            self.assertEqual('AWAITING_REVIEW', qa_compiled['status'])
            self.assertEqual(8, len(qa_compiled['steps'][1]['skills']))
            self.assertFalse(qa_compiled['can_execute'])
            architecture_lines = [line.split('ARCHITECTURE_WIZARD:', 1)[1]
                                  for line in test.stdout.splitlines()
                                  if line.startswith('ARCHITECTURE_WIZARD:')]
            self.assertEqual(1, len(architecture_lines), test.stdout)
            architecture_plan = json.loads(architecture_lines[0])
            compiled_architecture = validator.compile_workflow(architecture_plan)
            self.assertTrue(compiled_architecture['valid'], compiled_architecture['errors'])
            self.assertEqual(architecture_plan['constraints'], compiled_architecture['constraints'])
            self.assertEqual(architecture_plan['non_goals'], compiled_architecture['non_goals'])
            self.assertEqual(architecture_plan['tasks'][1]['architecture'],
                             compiled_architecture['steps'][1]['architecture'])
            self.assertEqual('NEEDS_DISCOVERY', compiled_architecture['steps'][1]['architecture_status'])
            self.assertFalse(compiled_architecture['can_execute'])
            self.assertFalse(compiled_architecture['authenticated_user_approval'])
            self.assertTrue(validator.compile_workflow(architecture_plan, require_approved=True)['errors'])
            architecture_cases = [line.split('ARCHITECTURE_CASES:', 1)[1]
                                  for line in test.stdout.splitlines()
                                  if line.startswith('ARCHITECTURE_CASES:')]
            self.assertEqual(1, len(architecture_cases), test.stdout)
            for case in json.loads(architecture_cases[0]):
                with self.subTest(change_type=case['tasks'][1]['architecture']['change_type'],
                                  source_host=case['tasks'][1]['architecture']['source_host']):
                    preview = validator.compile_workflow(case)
                    self.assertTrue(preview['valid'], preview['errors'])
                    self.assertEqual('NEEDS_DISCOVERY', preview['steps'][1]['architecture_status'])
                    self.assertFalse(preview['can_execute'])


if __name__ == "__main__":
    unittest.main()
