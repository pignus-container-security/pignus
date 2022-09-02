"""Controller Collecton - ApiKeys

"""

from flask import Blueprint, jsonify

from pignus_api.collects.api_keys import ApiKeys
from pignus_api.utils import auth


ctrl_api_keys = Blueprint('api_keys', __name__, url_prefix='/api-keys')


@ctrl_api_keys.route('')
@auth.auth_request
def index():
    """Get all ApiKeys
    """
    api_keys = ApiKeys().get_all()
    objectz = []
    for api_key in api_keys:
        objectz.append(api_key.json())

    data = {
        "objects": objectz,
        "object_type": "api_key",
        "object_count": len(objectz)
    }
    return jsonify(data)

# End File: pignus/src/pignus_api/controllers/ctrl_collections/ctrl_images.py
