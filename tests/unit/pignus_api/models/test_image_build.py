""" Test Model Image Build

"""

from pignus_api.models.image_build import ImageBuild


class TestImageBuild:

	def test____init__(self):
		"""Test the ImageBuild Model's initialization.
		:method: ImageBuild().__init__
		"""
		image_build = ImageBuild()
		assert hasattr(image_build, "table_name")
		assert hasattr(image_build, "digest")
		assert hasattr(image_build, "digest_local")
		assert hasattr(image_build, "image_id")
		assert hasattr(image_build, "repository")
		assert hasattr(image_build, "tags")

	def test____repr__(self):
		"""Test the ImageBuild Model's representation.
		:method: ImageBuild().__repr__
		"""
		image_build = ImageBuild()
		assert str(image_build) == "<ImageBuild>"

# End File: pignus/tests/pignus_api/models/test_image_build.py
