"""Regression Test Auth

"""

import os
import requests


PIGNUS_API_URL = os.environ.get("PIGNUS_API_URL")
PIGNUS_API_CLIENT_ID = "wrong-client"
PIGNUS_API_KEY = "wrong-key"
HEADERS = {
    "client-id": PIGNUS_API_CLIENT_ID,
    "x-api-key": PIGNUS_API_KEY
}


class TestOptions:

    def test__options(self):
        """Tests the Options collections through the Pignus Api
        GET /options
        """
        request_args = {
            "headers": HEADERS,
            "method": "GET",
            "url": "%s/options" % PIGNUS_API_URL,
        }

        response = requests.request(**request_args)
        assert response.status_code == 401


# End File: pignus/tests/regression/pignus_api/test_auth.py
