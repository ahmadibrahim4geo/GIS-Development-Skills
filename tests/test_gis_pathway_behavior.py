"""Exercise actual homepage GIS pathway JS filtering, counts and routes with Node.

This is a DOM-contract test, not a replacement for browser or GIS host testing.
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
const fs = require('node:fs');
const vm = require('node:vm');
const html = fs.readFileSync(process.argv[2], 'utf8');
const a=html.indexOf('const pathwaysData = [');
const b=html.indexOf('let activeCategory =',a);
const c=html.indexOf('function getTagBadgeClasses(',b);
const d=html.indexOf('function filterPathways(',c);
assert.ok(a>=0 && b>a && c>b && d>c, 'Homepage pathways JS declarations found');

let lang='en';
const dom={
  pathwaysContainer:{innerHTML:''},
  visibleCount:{innerText:''},
  pathwayTotal:{innerText:''}
};
const counts=['all','desktop','eo','dev'].flatMap(name=>[0,1].map(()=>({
  category:name,textContent:'',
  getAttribute(key){assert.equal(key,'data-pathway-count');return this.category}
})));
const document={
  documentElement:{getAttribute(name){assert.equal(name,'lang');return lang}},
  getElementById(id){assert.ok(dom[id],id);return dom[id]},
  querySelectorAll(selector){assert.equal(selector,'[data-pathway-count]');return counts}
};
const code=html.slice(a,b)+'\nlet activeCategory = "all";let currentSearch = "";\n'
  +html.slice(c,d)
  +'\n({pathwaysData,renderPathways,setFilters(cat,query){activeCategory=cat;currentSearch=query}})';
const api=vm.runInNewContext(code,{document});
assert.equal(api.pathwaysData.length,13);
assert.equal(new Set(api.pathwaysData.map(x=>x.id)).size,api.pathwaysData.length);
const qgisPlugin=api.pathwaysData.find(x=>x.id==='qgis');
const qgisEngine=api.pathwaysData.find(x=>x.id==='qgis-engine');
assert.ok(qgisPlugin && qgisEngine);
assert.match(qgisPlugin.url,/qgis-plugin-development\/SKILL\.md$/);
assert.match(qgisEngine.url,/qgis-engine-integration\/SKILL\.md$/);
assert.ok(qgisEngine.titleAr.includes('محرك'));
api.renderPathways();
assert.equal(dom.visibleCount.innerText,13);
assert.equal(dom.pathwayTotal.innerText,13);
for(const name of ['all','desktop','eo','dev']){
  const expected={all:13,desktop:5,eo:4,dev:4}[name];
  assert.ok(counts.filter(x=>x.category===name).every(x=>x.textContent===expected));
}
assert.match(dom.pathwaysContainer.innerHTML,/tabindex="0"/);
assert.match(dom.pathwaysContainer.innerHTML,/onkeydown=/);
api.setFilters('desktop','QGIS');
api.renderPathways();
assert.equal(dom.visibleCount.innerText,2);
assert.match(dom.pathwaysContainer.innerHTML,/QGIS Plugins/);
assert.match(dom.pathwaysContainer.innerHTML,/QGIS Engine Integration/);
api.setFilters('all','محرك QGIS');
lang='ar';
api.renderPathways();
assert.equal(dom.visibleCount.innerText,1);
assert.match(dom.pathwaysContainer.innerHTML,/aria-label="دمج محرك QGIS"/);
api.setFilters('all','does-not-exist-in-catalog');
api.renderPathways();
assert.equal(dom.visibleCount.innerText,0);
assert.match(dom.pathwaysContainer.innerHTML,/No matching development pathways/);
assert.match(dom.pathwaysContainer.innerHTML,/لا توجد مسارات تطوير مطابقة/);
console.log('Homepage GIS pathways DOM contract passed: 13 entries, 2 distinct QGIS routes, counts, search, Arabic and empty state.');
"""


class GisPathwayBehaviorTests(unittest.TestCase):
    def test_homepage_paths_are_real_and_bilingual(self):
        page=(ROOT/'index.html').read_text(encoding='utf-8')
        self.assertIn('data-pathway-count="all"',page)
        self.assertIn('data-pathway-count="desktop"',page)
        self.assertIn("qgis-engine-integration",page)
        self.assertIn("qgis-plugin-development",page)
        self.assertIn('role="button" tabindex="0"',page)
        self.assertIn("renderPathways(); // refresh localized",page)

    def test_pathway_js_actual_filtering_with_node(self):
        node=shutil.which('node')
        if not node:
            self.skipTest('Node is not installed; static contract still checked')
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'pathway-harness.cjs'
            path.write_text(HARNESS,encoding='utf-8')
            result=subprocess.run(
                [node,str(path),str(ROOT/'index.html')],
                capture_output=True,text=True,timeout=20)
            self.assertEqual(result.returncode,0,result.stdout+'\n'+result.stderr)


if __name__ == '__main__':
    unittest.main()
