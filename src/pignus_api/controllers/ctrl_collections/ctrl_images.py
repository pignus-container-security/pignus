"""Controller Collection - Images

"""

from flask import Blueprint, jsonify

from pignus_api.collects.images import Images
from pignus_api.utils import auth


ctrl_images = Blueprint('images', __name__, url_prefix='/images')


@ctrl_images.route('')
@auth.auth_request
def index():
    images = Images().get_all()

    ret_images = []
    for image in images:
        ret_images.append(image.json())

    data = {
        "objects": ret_images,
        "object_type": "image",
        "object_count": len(ret_images)
    }
    return jsonify(data)

# End File: pignus/src/pignus_api/controllers/ctrl_collections/ctrl_images.py
