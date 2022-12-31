"""Regression Test CTRL ApiKey
Checks that all routes on /api-key are working properly.

"""

import os
import requests


PIGNUS_API_URL = os.environ.get("PIGNUS_API_URL")
PIGNUS_API_CLIENT_ID = os.environ.get("PIGNUS_API_CLIENT_ID")
PIGNUS_API_KEY = os.environ.get("PIGNUS_API_KEY")
HEADERS = {
    "client-id": PIGNUS_API_CLIENT_ID,
    "x-api-key": PIGNUS_API_KEY
}


class TestApiApiKey:

    def test__api_key_get(self):
        """Tests the ApiKeys collections through the Pignus Api
        GET /api-keys
        """
        api_keys = self._get_all_api_keys()
        api_key = api_keys[0]
        request_args = {
            "headers": HEADERS,
            "method": "GET",
            "url": "%s/api-key/%s" % (PIGNUS_API_URL, api_key["id"]),
        }

        response = requests.request(**request_args)
        assert response.status_code == 200
        response_json = response.json()
        assert response_json["object_type"] == "api_key"

    def _get_all_api_keys(self):
        request_args = {
            "headers": HEADERS,
            "method": "GET",
            "url": "%s/api-keys" % PIGNUS_API_URL,
        }
        api_keys_resp = requests.request(**request_args).json()
        api_keys = api_keys_resp["objects"]
        return api_keys




# End File: pignus/tests/regression/pignus_api/test_ctrl_api_key.py
