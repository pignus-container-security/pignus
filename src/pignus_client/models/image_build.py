"""Pignus-Client: Model - Image Build

"""
from pignus_shared.models.image_build import FIELD_MAP
from pignus_client.models.base import Base


class ImageBuild(Base):

    def __init__(self):
        super(ImageBuild, self).__init__()
        self.entity_name = "image_build"
        self.field_map = FIELD_MAP
        self.setup()

    def __repr__(self) -> str:
        """
        """
        if self.digest:
            return "<ImageBuild %s:%s>" % (self.id)
        else:
            return "<ImageBuild>"


# End File: pignus/src/pignus_client/models/image_build.py
