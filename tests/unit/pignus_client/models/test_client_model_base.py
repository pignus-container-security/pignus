"""Pignus-Client: Unit test - Model - Base 

"""

from pignus_client.models.base import Base


class TestClientModelBase:

	def test____init__(self):
		"""Test the Base Model's initialization.
		:method: Base().__init__
		"""
		base = Base()
		assert hasattr(base, "entity_name")

	# def test____repr__(self):
	# 	"""Test the Base Model's representation.
	# 	:method: Base().__repr__
	# 	"""
	# 	base = Base()
	# 	assert str(base) == "<Base>"

	def test___create_total_map(self):
		"""
		:method: Base()._create_total_map()
		"""
		base = Base()
		base.field_map = [
            {
                "name": "extra_field",
                "type": "int",
            }
		]
		assert base._create_total_map()
		assert base.total_map[3]["name"] == "extra_field"

	def test___set_defaults(self):
		"""
		:method: Base()._set_defaults()
		"""
		base = Base()
		base.field_map = [
            {
                "name": "extra_field",
                "type": "int",
            }
		]
		base._create_total_map()
		assert base._set_defaults()
		assert hasattr(base, "id")
		assert hasattr(base, "created_ts")
		assert hasattr(base, "updated_ts")
		

# End File: pignus/tests/pignus_client/models/test_base.py
