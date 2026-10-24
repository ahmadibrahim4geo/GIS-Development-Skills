import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


class CatalogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.validator = load_module('catalog_validator', 'scripts/validate_catalog.py')
        cls.searcher = load_module('catalog_search', 'scripts/search_catalog.py')
        cls.catalog = json.loads((ROOT/'references/project-catalog.json').read_text(encoding='utf-8'))

    def test_catalog_valid(self):
        self.assertEqual([], self.validator.validate_catalog())

    def test_projects_at_least_twenty(self):
        self.assertGreaterEqual(len(self.catalog['projects']),20)

    def test_platform_search_arcmap(self):
        sources = self.searcher.search(self.catalog['projects'], platform='arcmap')
        self.assertTrue(sources)
        self.assertTrue(all('arcmap' in x['platforms'] for x in sources))

    def test_earthmapper_disambiguated(self):
        matches = self.searcher.search(self.catalog['projects'], query='EarthMapper')
        self.assertGreaterEqual(len(matches), 2)
        self.assertEqual(len({x['url'] for x in matches}), len(matches))

    def test_user_earthmapper_repositories_explicit(self):
        by_url = {x['url']:x for x in self.catalog['projects']}
        desktop = by_url['https://github.com/AliAlkazraji/EarthMapper']
        research = by_url['https://github.com/HIT-SIRS/EarthMapper']
        self.assertEqual('readme-only', desktop['source_availability'])
        self.assertEqual('design-reference-only', desktop['integration'])
        self.assertEqual('paper-assets-no-implementation', research['source_availability'])
        self.assertIn('research', research['integration'])

    def test_dotnet_backend_sources(self):
        links={x['url'] for x in self.catalog['projects']}
        for name in ('NetTopologySuite/NetTopologySuite', 'MicrosoftEdge/WebView2Samples', 'Esri/arcgis-pro-sdk'):
            self.assertIn('https://github.com/'+name, links)

    def test_archived_library_flag(self):
        for x in self.catalog['projects']:
            if x['url']=='https://github.com/haplokuon/netDxf':
                self.assertIn('archived', x['source_availability'])
                break
        else:
            self.fail('Expected archived DXF reference')

    def test_earthmapper_docs_exist(self):
        for path in ('references/earthmapper-case-studies.md', 'references/dotnet-gis.md', 'references/geoai-satellite-map.md'):
            self.assertTrue((ROOT/path).exists())

    def test_skill_frontmatter(self):
        text = (ROOT/'skills/gis-development/SKILL.md').read_text(encoding='utf-8')
        self.assertTrue(text.startswith('---\n'))
        self.assertIn('name: gis-development', text)
        self.assertIn('description:', text)


if __name__ == '__main__':
    unittest.main()