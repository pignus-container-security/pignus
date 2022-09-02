"""Controller Collection - Image Builds

"""

from flask import Blueprint, jsonify

from pignus_api.collects.image_builds import ImageBuilds
from pignus_api.utils import auth
from pignus_shared.utils import log

ctrl_image_builds = Blueprint("image_builds", __name__, url_prefix="/image-builds")


@ctrl_image_builds.route('')
@auth.auth_request
def index():
    image_builds = ImageBuilds().get_all()

    objectz = []
    for image_build in image_builds:
        objectz.append(image_build.json())

    data = {
        "objects": objectz,
        "object_type": "image_builds",
        "object_count": len(objectz)
    }
    return jsonify(data)


@ctrl_image_builds.route('/for-scan')
@auth.auth_request
def for_scan():
    """Get ImageBuilds ready for a scan."""
    image_builds = ImageBuilds().get_for_sentry_sync()

    log.info("for-scan")
    log.info(image_builds)

    objectz = []
    for image_build in image_builds:
        objectz.append(image_build.json())

    data = {
        "objects": objectz,
        "object_type": "image_builds",
        "object_count": len(objectz)
    }
    return jsonify(data)

# End File: pignus/src/pignus_api/controllers/ctrl_collections/ctrl_image_builds.py
