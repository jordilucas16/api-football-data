import unittest

from utils.utils import get_api_response, get_api_key, PREMIER_LEAGUE, SEASON, TOO_MANY_REQUESTS, get_total_pages


class Test_API_football(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("Loading data")
        cls._qs = {"league": PREMIER_LEAGUE, "season": SEASON, "page": 1}
        cls._url = "https://api-football-v1.p.rapidapi.com/v3/players"
        # Put your own API Key here ;-)
        cls._key = get_api_key()
        cls._response = get_api_response(cls._url, cls._qs, cls._key)
        cls._total_pages = get_total_pages()

    def test_get_api_football_response(self):
        print("Get API Football response Test")
        self.assertEqual(self._response.status_code, 200)
        self.assertNotEqual(self._response.status_code, 204)
        self.assertNotEqual(self._response.status_code, 400)
        self.assertNotEqual(self._response.status_code, 404)
        self.assertNotEqual(self._response.status_code, 500)
        self.assertNotEqual(self._response.status_code, TOO_MANY_REQUESTS)

    def test_get_total_pages(self):
        print("Get total pages Test")
        self.assertIsInstance(self._total_pages, int)
        self.assertNotIsInstance(self._total_pages, list)
        self.assertNotIsInstance(self._total_pages, tuple)
        self.assertNotIsInstance(self._total_pages, dict)