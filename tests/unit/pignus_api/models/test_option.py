""" Test Model Option

"""

from pignus_api.models.option import Option


class TestOption:

	def test____init__(self):
		"""Test the Option Model's initialization.
		:method: Option().__init__
		"""
		option = Option()
		assert hasattr(option, "table_name")
		assert hasattr(option, "name")
		assert hasattr(option, "type")
		assert hasattr(option, "value")

	def test____repr__(self):
		"""Test the Option Model's representation.
		:method: Option().__repr__
		"""
		option = Option()
		assert str(option) == "<Option>"

# End File: pignus/tests/pignus_api/models/test_option.py
