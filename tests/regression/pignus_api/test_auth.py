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


class TestAuth:

    def test__index(self):
        """Tests the index of Pignus Api
        GET /
        """
        request_args = {
            "headers": HEADERS,
            "method": "GET",
            "url": "%s" % PIGNUS_API_URL,
        }

        response = requests.request(**request_args)
        assert response.status_code == 200

    def test__api_keys(self):
        """Tests the ApiKeys collections of Pignus Api
        GET /api-keys
        """
        request_args = {
            "headers": HEADERS,
            "method": "GET",
            "url": "%s/api-keys" % PIGNUS_API_URL,
        }

        response = requests.request(**request_args)
        assert response.status_code == 401

    def test__images(self):
        """Tests the Images collections of Pignus Api
        GET /images
        """
        request_args = {
            "headers": HEADERS,
            "method": "GET",
            "url": "%s/images" % PIGNUS_API_URL,
        }

        response = requests.request(**request_args)
        assert response.status_code == 401

    def test__image_builds(self):
        """Tests the ImageBuilds collections of Pignus Api
        GET /image-builds
        """
        request_args = {
            "headers": HEADERS,
            "method": "GET",
            "url": "%s/image-builds" % PIGNUS_API_URL,
        }

        response = requests.request(**request_args)
        assert response.status_code == 401

    def test__image_clusters(self):
        """Tests the ImageClusters collections of Pignus Api
        GET /image-clusters
        """
        request_args = {
            "headers": HEADERS,
            "method": "GET",
            "url": "%s/image-clusters" % PIGNUS_API_URL,
        }

        response = requests.request(**request_args)
        assert response.status_code == 401

    def test__users(self):
        """Tests the Users collections through the Pignus Api
        GET /users
        """
        request_args = {
            "headers": HEADERS,
            "method": "GET",
            "url": "%s/users" % PIGNUS_API_URL,
        }

        response = requests.request(**request_args)
        assert response.status_code == 401

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
