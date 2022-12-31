"""Regression Test CTRL Users
Checks that all routes on /users are working properly.

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


class TestApiKey:

    def test__images_get(self):
        """Tests the Users collections through the Pignus Api
        GET /users
        """
        request_args = {
            "headers": HEADERS,
            "method": "GET",
            "url": "%s/users" % PIGNUS_API_URL,
        }

        response = requests.request(**request_args)
        assert response.status_code == 200
        response_json = response.json()
        assert "objects" in response_json
        assert "object_count" in response_json

        assert response_json["object_type"] == "user"
        assert response_json["object_count"] > 0


# End File: pignus/tests/regression/pignus_api/test_ctrl_images.py
