"""Pignus-Client: Model - Image

"""
from pignus_client.models.base import Base
from pignus_shared.models.image_build import FIELD_MAP


class Image(Base):

    def __init__(self):
        super(Image, self).__init__()
        self.entity_name = "image"
        self.field_map = FIELD_MAP
        self.setup()

    def __repr__(self):
        """Set the class representation
        :unit-test: TestImage::__repr__
        """
        if self.id:
            return "<Image %s:%s>" % (self.id, self.name)
        elif self.name:
            return "<Image %s>" % (self.name)
        else:
            return "<Image>"

# End File: pignus/src/pignus_client/models/image.py
