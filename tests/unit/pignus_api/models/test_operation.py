""" Test Model Operation

"""

from pignus_api.models.operation import Operation


class TestOperation:

	def test____init__(self):
		"""Test the Operation Model's initialization.
		:method: Operation().__init__
		"""
		operation = Operation()
		assert hasattr(operation, "table_name")

	def test____repr__(self):
		"""Test the operation Model's representation.
		:method: operation().__repr__
		"""
		operation = Operation()
		assert str(operation) == "<Operation>"

# End File: pignus/tests/pignus_api/models/test_operation.py
