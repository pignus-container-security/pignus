"""Controller Collects - Options

"""

from flask import Blueprint, jsonify

from pignus_api.collects.options import Options
from pignus_api.utils import auth

ctrl_options = Blueprint('options', __name__, url_prefix='/options')


@ctrl_options.route('')
@auth.auth_request
def index():
    options = Options().get_all_keyed()
    objectz = {}
    for option_name, option in options.items():
        objectz[option_name] = option.json()

    data = {
        "objects": objectz,
        "object_type": "options",
        "object_count": len(objectz)
    }
    return jsonify(data)

# End File: pignus/src/pignus_api/controllers/ctrl_collectioms/ctrl_options.py
