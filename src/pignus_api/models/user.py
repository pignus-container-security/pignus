"""User Model

"""
from werkzeug.security import check_password_hash

from pignus_api.collects.api_keys import ApiKeys
from pignus_api.models.base_entity_meta import BaseEntityMeta
from pignus_shared.utils import xlate


FIELD_MAP = [
    {
        "name": "name",
        "type": "str",
    },
    {
        "name": "last_login",
        "type": "datetime",
    },
    {
        "name": "role_id",
        "type": "int",
    },
    {
        "name": "client_id",
        "type": "str",
    },
    {
        "name": "client_secret",
        "type": "str",
    },
]


class User(BaseEntityMeta):

    model_name = "user"

    def __init__(self, conn=None, cursor=None):
        """Create the User instance.
        :unit-test: TestUser::test____init__
        """
        super(User, self).__init__(conn, cursor)
        self.table_name = "users"
        self.metas = {}
        self.field_map = FIELD_MAP
        self.api_writeable_fields = ["name", "role_id"]
        self.setup()

    def __repr__(self):
        """Class representation.
        :unit-test: TestUser::__repr__
        """
        if self.id:
            return "<User %s: %s>" % (self.id, self.name)
        else:
            return "<User>"

    def auth(self, client_id: str, api_key_raw: str) -> bool:
        """Check a User's auth ability."""
        sql = """
            SELECT * FROM `users`
            WHERE `client_id`="%s"
            LIMIT 1;""" % xlate.sql_safe(client_id)
        self.cursor.execute(sql)
        raw = self.cursor.fetchone()
        if not raw:
            return False
        self.build_from_list(raw)

        api_keys = ApiKeys().get_api_keys_for_user(self.id)

        for api_key in api_keys:
            if check_password_hash(api_key.key, api_key_raw):
                return True

        return False

    def delete(self) -> bool:
        """Delete a User and its ApiKeys."""
        user_api_keys = ApiKeys().get_api_keys_for_user(self.id)
        for user_key in user_api_keys:
            user_key.delete()

        super(User, self).delete()
        return True

    def disable(self) -> bool:
        """Disables a User by disabling all their ApiKeys."""
        api_keys = ApiKeys().get_api_keys_for_user()
        for api_key in api_keys:
            if api_key.enabled:
                api_key.enabled = False
                api_key.save()
        return True


# End File: pignus/src/pignus_api/models/user.py
