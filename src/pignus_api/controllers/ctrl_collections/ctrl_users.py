"""Controller Collects - Users

"""

from flask import Blueprint, jsonify

from pignus_api.collects.users import Users
from pignus_api.utils import auth

ctrl_users = Blueprint('users', __name__, url_prefix='/users')


@ctrl_users.route('')
@auth.auth_request
def index():
    users = Users().get_all()
    objectz = []

    for user in users:
        objectz.append(user.json())

    data = {
        "objects": objectz,
        "object_type": "user",
        "object_count": len(users)
    }

    return jsonify(data)

# End File: pignus/src/pignus_api/controllers/ctrl_collections/ctrl_users.py
