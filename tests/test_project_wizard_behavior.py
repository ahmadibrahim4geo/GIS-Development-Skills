"""Exercise the browser-only Project Wizard's real JS handlers in a Node DOM stub.

No network, package manager or paid browser services are required. This checks
generating a plan, bilingual switching, dirty-state invalidation and download.
"""
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
  type: ['desktop','pro','arcmap','dual','qgis','qgis-engine','web','remote','database','geoai'],
  locale: ['ar-en','en','multi'], files:['yes','no'], license:['free','host']
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
  'licenseLabel','detailsLabel','details','generate','download','resultLabel','result','status',
  'homeLink','roadmapLink','kmlLink','reliabilityLink','wizardPrivacy']) node(id);
node('download').disabled = true;
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
e('details').value='Preserve icons, folders and styles.';
e('generate').onclick();
assert.equal(e('download').disabled,false);
assert.match(e('result').textContent,/GIS Project Implementation Plan/);
assert.match(e('result').textContent,/KML\/KMZ/);
assert.match(e('result').textContent,/Preserve icons/);
e('download').onclick();
assert.equal(lastLink.download,'gis-project-plan-en.md');
assert.equal(lastLink.clicked,true);
assert.match(lastBlob.parts[0],/Project Implementation Plan/);
assert.equal(revoke,'blob:plan');
e('type').value='qgis';
e('type').fire('change');
assert.equal(e('download').disabled,true);
assert.equal(e('result').textContent,'');
e('generate').onclick();
assert.match(e('result').textContent,/PyQGIS/);
assert.match(e('result').textContent,/skills\/qgis-plugin-development\/SKILL.md/);
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


if __name__ == "__main__":
    unittest.main()
