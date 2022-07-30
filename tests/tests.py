import unittest

from utils.utils import get_api_response, get_api_key, PREMIER_LEAGUE, SEASON, TOO_MANY_REQUESTS


class Test_API_football(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("Loading data")
        cls._qs = {"league": PREMIER_LEAGUE, "season": SEASON, "page": 1}
        cls._url = "https://api-football-v1.p.rapidapi.com/v3/players"
        # Put your own API Key here ;-)
        cls._key = get_api_key()

    def test_get_api_football_response(self):
        print("Get API Football response Test")
        self.assertEqual(get_api_response(self._url, self._qs, self._key).status_code, 200)
        self.assertNotEqual(get_api_response(self._url, self._qs, self._key).status_code, 400)
        self.assertNotEqual(get_api_response(self._url, self._qs, self._key).status_code, 404)
        self.assertNotEqual(get_api_response(self._url, self._qs, self._key).status_code, 500)
        self.assertNotEqual(get_api_response(self._url, self._qs, self._key).status_code, TOO_MANY_REQUESTS)
