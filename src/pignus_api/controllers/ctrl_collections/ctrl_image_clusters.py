"""Controller Collection - Image Clusters

"""

from flask import Blueprint, jsonify

from pignus_api.collects.image_clusters import ImageClusters
from pignus_api.utils import auth

ctrl_image_clusters = Blueprint("image_clusters", __name__, url_prefix="/image-clusters")


@ctrl_image_clusters.route('')
@auth.auth_request
def index():
    image_clusters = ImageClusters().get_all()

    objectz = []
    for image_build in image_clusters:
        objectz.append(image_build.json())

    data = {
        "objects": objectz,
        "object_type": "image_cluster",
        "object_count": len(objectz)
    }
    return jsonify(data)


# End File: pignus/src/pignus_api/controllers/ctrl_collections/ctrl_image_clusters.py
