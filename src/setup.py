#!/usr/bin/env python3

from setuptools import setup
from pignus_api import version

setup(
    name="pignus",
    version=version.__version__,
    description="Pignus",
    author="Alix",
    author_email="alix@politeauthority.io",
    url="https://github.com/politeauthority/pignus",
    packages=[
        "pignus_api",
        "pignus_api.collects",
        "pignus_api.controllers",
        "pignus_api.controllers.ctrl_collections",
        "pignus_api.controllers.ctrl_models",
        "pignus_api.models",
        "pignus_api.utils",
        "pignus_client",
        "pignus_client.models",
        "pignus_sentry",
        "pignus_shared",
        "pignus_shared.utils",
        "pignus_shared.models",
    ],
    # scripts=["scripts/pignus"],
)

# End File: pignus/src/setup.py
