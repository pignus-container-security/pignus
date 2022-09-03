"""Controller Model - Api Key

"""

from flask import Blueprint, jsonify

from pignus_api.controllers.ctrl_models import ctrl_base
from pignus_api.models.api_key import ApiKey
from pignus_api.utils import auth

ctrl_api_key = Blueprint('api-key', __name__, url_prefix='/api-key')


@ctrl_api_key.route("/<api_key_id>")
@auth.auth_request
def get_model(api_key_id: int):
    """GET operation for a ApiKey.
    GET /api-key
    """
    data = ctrl_base.get_model(ApiKey, api_key_id)
    if not isinstance(data, dict):
        return data

    return jsonify(data)


@ctrl_api_key.route("/<api_key_id>", methods=["POST"])
@ctrl_api_key.route("", methods=["POST"])
@auth.auth_request
def post_model(api_key_id: int = None):
    """Create or modify an ApiKey."""
    data = ctrl_base.post_model(ApiKey, api_key_id)
    return jsonify(data), 201


@ctrl_api_key.route("/<api_key_id>", methods=["DELETE"])
@auth.auth_request
def delete_model(api_key_id: int = None):
    """DELETE opperation for a Api Key.
    DELETE /api-key
    """
    data = ctrl_base.delete_model(ApiKey, api_key_id)
    if not isinstance(data, dict):
        return data

    return jsonify(data), 201


# End File: pignus/src/pignus_api/controllers/ctrl_modles/ctrl_api_key.py
