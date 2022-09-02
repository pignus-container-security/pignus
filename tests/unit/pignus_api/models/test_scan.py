""" Test Model Scan

"""

from pignus_api.models.scan import Scan


class TestScan:

	def test____init__(self):
		"""Test the Scan Model's initialization.
		:method: Scan().__init__
		"""
		scan = Scan()
		assert hasattr(scan, "table_name")
		assert hasattr(scan, "metas")

	def test____repr__(self):
		"""Test the Scan Model's representation.
		:method: Scan().__repr__
		"""
		scan = Scan()
		assert str(scan) == "<Scan>"


# End File: pignus/tests/pignus_api/models/test_Scan.py
