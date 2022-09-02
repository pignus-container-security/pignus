"""Controller Model - Image

"""

from flask import Blueprint, request, jsonify, Response

from pignus_api.controllers.ctrl_models import ctrl_base
from pignus_api.models.image import Image
from pignus_api.models.image_build import ImageBuild
from pignus_api.utils import auth
from pignus_shared.utils import misc
from pignus_shared.utils import log

ctrl_image = Blueprint('image', __name__, url_prefix='/image')


@ctrl_image.route("")
@ctrl_image.route("/<image_id>")
@auth.auth_request
def get_model(image_id: int = None) -> Response:
    """GET operation for a Image.
    GET /image
    """
    data = ctrl_base.get_model(Image, image_id)
    if not isinstance(data, dict):
        return data

    return jsonify(data)


@ctrl_image.route("", methods=["POST"])
@ctrl_image.route("/<image_id>", methods=["POST"])
@auth.auth_request
def post_model(image_id: int = None):
    """POST operation for a Image.
    """
    resp_data = {
        "status": "Success",
        "object": {},
        "object_type": "image",
    }

    request_data = request.get_json()
    if "name" not in request_data:
        resp_data["status"] = "Error"
        return jsonify(resp_data)

    image_parsed = misc.parse_image_url(request_data["name"])

    image = Image().check_image_exists(image_parsed)

    if not image:
        image = Image()

    image.name = image_parsed["name"]
    image.maintained = True
    image.repositories = [image_parsed["repository"]]
    image.save()

    print("\n\n")
    print(image)

    print(image_parsed)
    print("\n\n")
    resp_data["ext"] = image_parsed
    resp_data["object"] = image.json()
    return jsonify(resp_data)


@ctrl_image.route("/<image_id>", methods=["DELETE"])
@auth.auth_request
def delete_model(image_id: int = None) -> Response:
    """DELETE opperation for a Image.
    DELETE /image
    """
    data = ctrl_base.delete_model(Image, image_id)
    if not isinstance(data, dict):
        return data

    return jsonify(data), 201


@ctrl_image.route("/add", methods=["POST"])
@auth.auth_request
def add() -> Response:
    """Route for adding an Image and ImageBuild in a single request.
    POST /image/add
    """
    request_data = request.get_json()
    do_create_image = False
    do_create_image_build = False
    image = Image()

    if not image.get_by_name(request_data["name"]):
        do_create_image = True
        do_create_image_build = True
    else:
        do_create_image = False

    if do_create_image:
        image = create_image(request_data)

    image_build = ImageBuild()
    if not image_build.get_by_digest(request_data["digest"]):
        do_create_image_build = True

    if do_create_image_build:
        image_build = ImageBuild()
        if not image_build.get_by_digest(request_data["digest"]):
            image_build = create_image_build(image, request_data)

    log.info(image)
    log.info(image_build)
    data = {
        "status": "Error",
        "message": "",
        "object": image.json(),
        "object_type": "image"
    }

    return jsonify(data), 201


def create_image(image_url: dict) -> Image:
    """Create an Image from the image_url."""
    image = Image()
    image.name = image_url["name"]
    image.repositories = [image_url["repository"]]
    image.save()
    log.info("Created: %s" % image)
    return image


def create_image_build(image: Image, image_url: dict) -> ImageBuild:
    """Create an ImageBuild from an Image and the image_url."""
    image_build = ImageBuild()
    image_build.image_id = image.id
    if "digest" in image_url:
        image_build.digest = image_url["digest"]
    if "tag" in image_url:
        image_build.tag = image_url["tag"]
    if "repository" in image_url:
        image_build.repository = image_url["repository"]
    image_build.scan_flag = True
    image_build.save()
    log.info("Created: %s" % image_build)
    return image_build


# End File: pignus/src/pignus_api/controllers/ctrl_modles/ctrl_image.py
