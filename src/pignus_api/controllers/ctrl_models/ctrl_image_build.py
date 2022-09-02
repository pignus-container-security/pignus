"""Controller Model - Image Build

"""

from flask import Blueprint, jsonify

from pignus_api.controllers.ctrl_models import ctrl_base
from pignus_api.models.image_build import ImageBuild
from pignus_api.utils import auth

ctrl_image_build = Blueprint('image_build', __name__, url_prefix='/image-build')


@ctrl_image_build.route("")
@ctrl_image_build.route("/<image_build_id>")
@auth.auth_request
def get_model(image_build_id: int = None):
    """GET opperation for an ImageBuild
    """
    data = ctrl_base.get_model(ImageBuild, image_build_id)
    if not isinstance(data, dict):
        return data

    return jsonify(data)


@ctrl_image_build.route("", methods=["POST"])
@ctrl_image_build.route("/<image_build_id>", methods=["POST"])
@auth.auth_request
def post_model(image_build_id: int = None):
    """Create a new User."""
    data = ctrl_base.post_model(ImageBuild, image_build_id)
    if not isinstance(data, dict):
        return data
    return jsonify(data), 201


@ctrl_image_build.route("/<image_build_id>", methods=["DELETE"])
@auth.auth_request
def delete_model(image_build_id: int = None):
    """DELETE opperation for ImageBuild.
    """
    data = ctrl_base.delete_model(ImageBuild, image_build_id)
    if not isinstance(data, dict):
        return data

    return jsonify(data), 201


# End File: pignus/src/pignus_api/controllers/ctrl_modles/ctrl_image_build.py
