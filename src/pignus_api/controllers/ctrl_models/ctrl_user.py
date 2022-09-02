"""Controller Model - User

"""

from flask import Blueprint, jsonify

from pignus_api.controllers.ctrl_models import ctrl_base
from pignus_api.models.user import User
from pignus_api.utils import auth


ctrl_user = Blueprint('user', __name__, url_prefix='/user')


@ctrl_user.route("")
@ctrl_user.route("/<user_id>")
@auth.auth_request
def get_model(user_id: int):
    data = ctrl_base.get_model(User, user_id)
    return jsonify(data)


@ctrl_user.route("", methods=["POST"])
@ctrl_user.route("/<user_id>", methods=["POST"])
@auth.auth_request
def post_model(user_id: int = None):
    """Create a new User."""
    data = ctrl_base.post_model(User, user_id)
    return jsonify(data), 201


@ctrl_user.route("/<user_id>", methods=["DELETE"])
@auth.auth_request
def delete_model(user_id: int):
    """Delete a User."""
    resp_data = {
        "status": "Success"
    }

    user = User()
    if not user.get_by_id(user_id):
        resp_data["status"] = "Error"
        resp_data["message"] = "User not found"
        return jsonify(resp_data), 404
    user.delete()
    resp_data["message"] = "User deleted successfully"
    resp_data["object"] = user.json()
    resp_data["object_type"] = "user"
    return jsonify(resp_data), 201

# End File: pignus/src/pignus_api/controllers/ctrl_modles/ctrl_user.py
