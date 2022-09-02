""" Test Model Base

"""

from pignus_api.models.base import Base


class TestBase:

	def test____init__(self):
		"""Test the Base Model's initialization.
		:method: Base().__init__
		"""
		base = Base()
		assert hasattr(base, "table_name")
		assert hasattr(base, "backend")
		assert hasattr(base, "base_map")
		assert hasattr(base, "field_map")

	def test____repr__(self):
		"""Test the Base Model's representation.
		:method: Base().__repr__
		"""
		base = Base()
		assert str(base) == "<Base>"

# End File: pignus/tests/pignus_api/models/test_base.py
