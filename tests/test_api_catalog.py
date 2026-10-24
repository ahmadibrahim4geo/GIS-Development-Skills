import importlib.util
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def module(name,path):
    spec=importlib.util.spec_from_file_location(name,ROOT/path)
    result=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result

class APICatalogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.validator=module('api_validator','scripts/validate_api_catalog.py')
        cls.searcher=module('api_search','scripts/search_api_catalog.py')
        cls.catalog=json.loads((ROOT/'references/free-geospatial-apis.json').read_text(encoding='utf-8'))

    def test_schema_valid(self):
        self.assertEqual([],self.validator.validate_catalog())

    def test_multiple_domains(self):
        self.assertGreaterEqual(len(self.catalog['services']),15)
        self.assertGreaterEqual(len({s['category'] for s in self.catalog['services']}),7)

    def test_critical_provider_limits(self):
        sources={s['id']:s for s in self.catalog['services']}
        self.assertEqual('free-key-required',sources['opentopography']['access'])
        self.assertEqual('temporarily-unavailable',sources['soilgrids']['access'])
        self.assertEqual('restricted-public',sources['nominatim']['access'])
        self.assertEqual('free-noncommercial',sources['open-meteo-forecast']['access'])
        self.assertIn('offline',sources['openfreemap']['limits'])

    def test_filter(self):
        hits=self.searcher.search(self.catalog['services'],category='terrain-elevation')
        self.assertGreaterEqual(len(hits),3)
        self.assertTrue(all(x['category']=='terrain-elevation' for x in hits))

    def test_parent_projects(self):
        projects=json.loads((ROOT/'references/project-catalog.json').read_text(encoding='utf-8'))['projects']
        by_url={p['url']:p for p in projects}
        self.assertEqual('MIT (LICENSE.md verified)',by_url['https://github.com/opengeos/geolibre-r']['license'])
        self.assertIn('Apache-2.0',by_url['https://github.com/opengeos/RustGIS']['license'])

if __name__=='__main__':
    unittest.main()