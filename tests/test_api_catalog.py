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

    def test_free_first_cost_tiers(self):
        entries=self.catalog['services']
        tiers={x['cost_tier'] for x in entries}
        self.assertEqual(tiers,{'free-self-hosted','free-conditional','restricted','trial','commercial','unavailable'})
        self.assertEqual(sum(x["cost_tier"] in ("free-self-hosted","free-conditional") for x in entries),len(self.searcher.search(entries,free_only=True)))
        self.assertFalse(any(x['cost_tier'] in ('commercial','trial','restricted','unavailable') for x in self.searcher.search(entries,free_only=True)))
        self.assertEqual([],self.searcher.search(entries,cost_tier='unrecognized'))

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

    def test_2026_expanded_apis_and_migrations(self):
        src={s['id']:s for s in self.catalog['services']}
        ids={'geoboundaries','worldpop-v2','geonames','nasa-firms',
             'usgs-earthquake','nasa-cmr','openaq-v3','open-meteo-air-quality',
             'open-meteo-flood','ohsome-v2','openrouteservice-heigit',
             'hdx-hapi','usgs-waterdata','noaa-coops','nasa-eonet',
             'worldbank-indicators','noaa-ncei-cdo','noaa-ncei-erddap',
             'inaturalist'}
        # Required providers and unique IDs matter; valid additions may grow the catalog.
        self.assertTrue(ids.issubset(src))
        self.assertEqual('free-key-required',src['openaq-v3']['access'])
        self.assertEqual('free-noncommercial',src['open-meteo-flood']['access'])
        self.assertIn('/ohsome-api/v2/',src['ohsome-v2']['service_url'])
        self.assertNotIn('v2-rc',src['ohsome-v2']['service_url'])
        self.assertIn('early 2027',src['usgs-waterdata']['caveat'])
        self.assertEqual(len(src),len(self.catalog['services']))

    def test_gebco_2026_api_access_and_safety(self):
        entries={s['id']:s for s in self.catalog['services']}
        wms=entries['gebco-2026-wms']
        grid=entries['gebco-2026-ceda-opendap']
        self.assertIn('wms.gebco.net',wms['service_url'])
        self.assertEqual(wms['authentication'],'none')
        self.assertIn('OPeNDAP',grid['formats'])
        self.assertIn('gebco_2026',grid['service_url'])
        self.assertIn('TID',grid['caveat'])
        self.assertIn('navigation',wms['caveat'])
        self.assertNotEqual(wms['service_url'],grid['service_url'])

    def test_geocoding_pricing_groups_order_and_safety(self):
        services=[s for s in self.catalog['services'] if s['category']=='geocoding']
        self.assertEqual(15,len(services))
        self.assertGreaterEqual(len(self.catalog['services']),52)
        groups=['self-hosted-open-source','public-fair-use','free-with-quota','trial-only','commercial']
        self.assertEqual(sorted(services,key=lambda s:groups.index(s['pricing_group'])),services)
        by_id={s['id']:s for s in services}
        self.assertTrue({'nominatim','geonames','pelias-self-hosted','photon-komoot',
                         'open-meteo-geocoding','geoapify-geocoding','locationiq-geocoding',
                         'geocode-maps-co','arcgis-world-geocoding','maptiler-geocoding',
                         'opencage-geocoding','google-places-new','mapbox-search-box',
                         'here-search','tomtom-search'}.issubset(by_id))
        self.assertIn('no autocomplete',by_id['nominatim']['limits'].lower())
        self.assertIn('TESTING ONLY',by_id['opencage-geocoding']['limits'])
        self.assertEqual('commercial',by_id['google-places-new']['pricing_group'])

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