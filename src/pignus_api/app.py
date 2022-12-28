#!/usr/bin/env python
"""Pignus Api

"""
import logging

from flask import Flask, jsonify

from pignus_api.collects.options import Options
from pignus_api.controllers.ctrl_models.ctrl_image import ctrl_image
from pignus_api.controllers.ctrl_models.ctrl_image_build import ctrl_image_build
from pignus_api.controllers.ctrl_models.ctrl_user import ctrl_user
from pignus_api.controllers.ctrl_collections.ctrl_api_keys import ctrl_api_keys
from pignus_api.controllers.ctrl_collections.ctrl_images import ctrl_images
from pignus_api.controllers.ctrl_collections.ctrl_image_builds import ctrl_image_builds
from pignus_api.controllers.ctrl_collections.ctrl_options import ctrl_options
from pignus_api.controllers.ctrl_collections.ctrl_users import ctrl_users
from pignus_api.migrate import Migrate
from pignus_api.utils import db
from pignus_api.utils import glow

Migrate().run()
app = Flask(__name__)
app.config.update(DEBUG=True)


def register_blueprints(app: Flask):
    """Connect the blueprints to the router."""
    app.register_blueprint(ctrl_image)
    app.register_blueprint(ctrl_image_build)
    app.register_blueprint(ctrl_user)
    app.register_blueprint(ctrl_api_keys)
    app.register_blueprint(ctrl_images)
    app.register_blueprint(ctrl_image_builds)
    app.register_blueprint(ctrl_options)
    app.register_blueprint(ctrl_users)
    return True


@app.route('/')
def index():
    data = {
        "info": "Pignus Api",
        "version": "0.0.1"
    }
    return jsonify(data)


@app.route('/debug')
def debug():
    html = "<html><head><title>debug</title></head><body></body></html>"
    return html


if __name__ == "__main__":
    glow.db = db.connect()
    glow.options = Options().load_options()
    register_blueprints(app)
    app.run(host='0.0.0.0', port=5001)

elif __name__ != '__main__':
    glow.db = db.connect()
    glow.options = Options().load_options()
    register_blueprints(app)
    gunicorn_logger = logging.getLogger('gunicorn.info')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)


# End File: pignus/src/pignus_api/app.py
