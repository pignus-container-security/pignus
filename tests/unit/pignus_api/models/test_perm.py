""" Test Model Perm

"""

from pignus_api.models.perm import Perm


class TestPerm:

	def test____init__(self):
		"""Test the Perm Model's initialization.
		:method: Perm().__init__
		"""
		perm = Perm()
		assert hasattr(perm, "table_name")
		assert hasattr(perm, "name")
		assert hasattr(perm, "slug_name")

	def test____repr__(self):
		"""Test the Perm Model's representation.
		:method: Perm().__repr__
		"""
		perm = Perm()
		assert str(perm) == "<Perm>"


# End File: pignus/tests/pignus_api/models/test_perm.py
