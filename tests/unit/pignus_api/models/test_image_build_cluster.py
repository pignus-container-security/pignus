""" Test Model Image Build Cluster

"""

from pignus_api.models.image_build_cluster import ImageBuildCluster


class TestImageBuildCluster:

	def test____init__(self):
		"""Test the ImageBuildCluster Model's initialization.
		:method: ImageBuildCluster().__init__
		"""
		image_build_cluster = ImageBuildCluster()
		assert hasattr(image_build_cluster, "table_name")

	def test____repr__(self):
		"""Test the ImageBuildCluster Model's representation.
		:method: ImageBuildCluster().__repr__
		"""
		image_build_cluster = ImageBuildCluster()
		assert str(image_build_cluster) == "<ImageBuildCluster>"

# End File: pignus/tests/pignus_api/models/test_image_build_cluster.py
