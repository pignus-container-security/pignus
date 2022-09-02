""" Test Model Image

"""

from pignus_api.models.image import Image


class TestImage:

	def test____init__(self):
		"""Test the Image Model's initialization.
		:method: Image().__init__
		"""
		image = Image()
		assert hasattr(image, "name")
		assert hasattr(image, "repositories")
		assert hasattr(image, "maintained")
		assert hasattr(image, "state")
		assert hasattr(image, "state_msg")

	def test____repr__(self):
		"""Test the Image Model's representation.
		:method: Image().__repr__
		"""
		image = Image()
		assert str(image) == "<Image>"


# End File: pignus/tests/pignus_api/models/test_image.py
