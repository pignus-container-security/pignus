"""Regression Test CTRL Images
Checks that all routes on /images are working properly.

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
        """Tests the Images collections through the Pignus Api
        GET /images
        """
        request_args = {
            "headers": HEADERS,
            "method": "GET",
            "url": "%s/images" % PIGNUS_API_URL,
        }

        response = requests.request(**request_args)
        assert response.status_code == 200
        response_json = response.json()
        assert response_json["object_type"] == "image"
        assert "objects" in response_json
        assert "object_count" in response_json


# End File: pignus/tests/regression/pignus_api/test_ctrl_images.py
