""" Test Model User

"""

from pignus_api.models.user import User


class TestUser:

	def test____init__(self):
		"""Test the User Model's initialization.
		:method: User().__init__
		"""
		user = User()
		user.name = "TestUser"
		assert user.name

	def test____repr__(self):
		"""Test the ApiKey Model's representation.
		:method: ApiKey().__repr__
		"""
		user = User()
		assert str(user) == "<User>"


# End File: pignus/tests/pignus_api/models/test_user.py
