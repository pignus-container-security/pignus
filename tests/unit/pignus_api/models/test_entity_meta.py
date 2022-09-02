""" Test Model EntityMeta

"""

from pignus_api.models.entity_meta import EntityMeta


class TestEntityMeta:

	def test____init__(self):
		"""Test the Entity Meta Model's initialization.
		:method: EntityMeta().__init__
		"""
		entity_meta = EntityMeta()
		assert hasattr(entity_meta, "table_name")

	def test____repr__(self):
		"""Test the EntityMeta Model's representation.
		:method: EntityMeta().__repr__
		"""
		entity_meta = EntityMeta()
		assert str(entity_meta) == "<EntityMeta>"

# End File: pignus/tests/pignus_api/models/test_base.py
