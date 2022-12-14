"""Pignus Client

"""
import requests
import os

from pignus_client.models.image import Image
from pignus_client.models.image_build import ImageBuild
from pignus_shared.utils import log


class PignusClient:

    def __init__(self, api_url: str = None, api_client_id: str = None, api_key: str = None):
        """
        :unit-test: TestRest::test____init__()
        """
        if api_url:
            self.api_url = api_url
        else:
            self.api_url = os.environ.get("PIGNUS_API_URL")

        if api_client_id:
            self.api_client_id = api_client_id
        else:
            self.api_client_id = os.environ.get("PIGNUS_API_CLIENT_ID")

        if api_key:
            self.api_key = api_key
        else:
            self.api_key = os.environ.get("PIGNUS_API_KEY")

        self.die_response_level = None
        self.headers = {
            "x-api-key": self.api_key,
            "client-id": self.api_client_id,
            "Content-Type": "application/json",
            # "User-Agent": settings.client["API_UA"],
        }

    def __repr__(self):
        return "<PignusClient %s>" % self.api_url

    def image_add(self, payload: dict = {}) -> dict:
        """Submit a potentially new Image to the Pignus Api, which will be translated to a new
        ImageBuild on the server.
        """
        response = self.request("image/add", payload, "POST")
        return response

    def image_get_by_id(self, image_id: int) -> dict:
        """Get Images on the Pignus Api, against /image/{image_id}
        """
        response = self.request("image/%s" % image_id)
        return response

    def images_get(self, payload: dict = {}) -> dict:
        """Get Images on the Pignus Api, against /images
        :unit-test: TestRest:test__images_get
        """
        response = self.request("images", payload)
        return response

    def image_builds_get_for_scan(self, payload: dict = {}) -> dict:
        """Get Images on the Pignus Api, against /images
        :unit-test: TestRest:test__images_get
        """
        response = self.request("image-builds/for-scan", payload)
        return response

    def object_get_by_id(self, entity_name: str, entity_id: int):
        """Get a supported model back from the Pignus Api."""
        supported_entities = ["image", "image_build"]
        if entity_name not in supported_entities:
            log.error("Not supported entity for object_get_by_id: %s" % entity_name)
            return False
        response = self.request("%s/%s" % (entity_name, entity_id))
        print(response.url)
        if response.status_code != 200:
            log.warning("Could not find %s with ID %s" % (entity_name, entity_id))
            return False

        response_json = response.json()
        ret = None
        if entity_name == "image":
            ret = Image()
        elif entity_name == "image_build":
            ret = ImageBuild()

        ret.build_from_dict(response_json["object"])

        return ret

    def request(
        self, url: str, payload: dict = {}, method: str = "GET"
    ) -> requests.Response:
        """Make a request on the Pignus Api.
        :unit-test: TestClient:test__request
        """
        request_args = {
            "headers": self.headers,
            "method": method,
            "url": "%s/%s" % (self.api_url, url),
        }
        if payload:
            if request_args["method"] in ["GET", "DELETE"]:
                request_args["params"] = payload
            elif request_args["method"] == "POST":
                for key, value in payload.items():
                    if isinstance(value, bool):
                        payload[key] = str(value).lower()
                request_args["json"] = payload

        response = requests.request(**request_args)
        if response.status_code >= 500:
            log.error("Pignus Api Error")

        if self.die_response_level:
            if response.status_code >= self.die_response_level:
                print("-- Request Failed --")
                print("Url\t%s" % request_args["url"])
                print("Status\t%s" % response.status_code)
                print("Method\t%s" % request_args["method"])
                # if payload:
                #     print("Params\t%s" % payload)
                print("Response")
                print(response.text)

        return response

# End File: pignus/src/pignus_client/__init__.py
