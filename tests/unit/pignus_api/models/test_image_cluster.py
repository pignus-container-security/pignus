""" Test Model Image Build Cluster

"""

from pignus_api.models.image_cluster import ImageCluster


class TestImageCluster:

	def test____init__(self):
		"""Test the ImageCluster Model's initialization.
		:method: ImageCluster().__init__
		"""
		image_cluster = ImageCluster()
		assert hasattr(image_cluster, "table_name")

	def test____repr__(self):
		"""Test the ImageCluster Model's representation.
		:method: ImageCluster().__repr__
		"""
		image_cluster = ImageCluster()
		assert str(image_cluster) == "<ImageCluster>"

# End File: pignus/tests/pignus_api/models/test_image_cluster.py
