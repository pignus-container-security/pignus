""" Test Model ApiKey

"""

from pignus_api.models.api_key import ApiKey


class TestApiKey:

	def test____init__(self):
		"""Test the ApiKey Model's initialization.
		:method: ApiKey().__init__
		"""
		api_key = ApiKey()
		assert hasattr(api_key, "key")
		assert hasattr(api_key, "user_id")
		assert hasattr(api_key, "enabled")
		assert hasattr(api_key, "last_use")
		assert hasattr(api_key, "expiration")

	def test____repr__(self):
		"""Test the ApiKey Model's representation.
		:method: ApiKey().__repr__
		"""
		base = ApiKey()
		assert str(base) == "<ApiKey>"


# End File: pignus/tests/pignus_api/models/test_api_key.py
