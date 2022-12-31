"""Regression Test CTRL User
Checks that all routes on /user are working properly.

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


class TestApiUsers:

    def test__user_get(self):
        """Tests the User model through the Pignus Api
        GET /user
        """
        users = self._get_all_users()
        user = users[0]
        request_args = {
            "headers": HEADERS,
            "method": "GET",
            "url": "%s/user/%s" % (PIGNUS_API_URL, user["id"]),
        }
        users = requests.request(**request_args)
        response = requests.request(**request_args)
        assert response.status_code == 200
        response_json = response.json()
        assert response_json["object_type"] == "user"

    def _get_all_users(self):
        request_args = {
            "headers": HEADERS,
            "method": "GET",
            "url": "%s/users" % PIGNUS_API_URL,
        }
        users_resp = requests.request(**request_args).json()
        users = users_resp["objects"]
        return users



# End File: pignus/tests/regression/pignus_api/test_ctrl_user.py
