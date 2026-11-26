"""Offline tests: no provider requests, user keys, or quota consumed."""
import importlib.util
import io
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PATH=ROOT/"examples"/"geocoding"/"place_search.py"
spec=importlib.util.spec_from_file_location("place_search_example",PATH)
search=importlib.util.module_from_spec(spec)
spec.loader.exec_module(search)

class GeocodingExampleTests(unittest.TestCase):
    def test_open_meteo_config_no_key(self):
        host,p=search.provider_config("open-meteo-geocoding","القاهرة",environ={})
        self.assertEqual("EG",p["countryCode"])
        self.assertTrue(host.startswith("https://"))
        self.assertEqual("القاهرة",p["name"])

    def test_credentials_required(self):
        with self.assertRaises(search.GeocodingError):
            search.provider_config("geonames","Aswan",environ={})
        with self.assertRaises(search.GeocodingError):
            search.provider_config("geoapify-geocoding","Cairo",environ={})

    def test_mock_response_and_axis_order(self):
        payload={"results":[{"name":"القاهرة","latitude":30.04,"longitude":31.24,"id":123}]}
        class Reply:
            def __enter__(self): return io.BytesIO(json.dumps(payload).encode())
            def __exit__(self,*_): return None
        def opener(request,timeout):
            self.assertIn("countryCode=EG",request.full_url)
            self.assertEqual(12,timeout)
            return Reply()
        got=search.search_places("open-meteo-geocoding","Cairo",opener=opener,environ={})
        self.assertEqual([31.24,30.04],got[0]["coordinates"])
        self.assertEqual("EPSG:4326",got[0]["crs"])

    def test_geoapify_and_geonames_normalization(self):
        geo=search.normalize("geonames",{"geonames":[{"toponymName":"Aswan","lat":"24.09","lng":"32.90"}]})
        self.assertEqual([32.9,24.09],geo[0]["coordinates"])
        api=search.normalize("geoapify-geocoding",{"results":[{"formatted":"Cairo, Egypt","lat":30.1,"lon":31.2}]})
        self.assertEqual("Cairo, Egypt",api[0]["name"])

    def test_invalid_coordinate_discarded(self):
        self.assertEqual([],search.normalize("open-meteo-geocoding",{"results":[{"name":"x","latitude":999,"longitude":300}]}))

    def test_provider_errors_are_explicit(self):
        with self.assertRaises(search.GeocodingError):
            search.normalize("geonames",{"status":{"message":"quota exceeded"}})

if __name__=="__main__":
    unittest.main()
