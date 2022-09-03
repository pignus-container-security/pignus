"""ApiKey Model

"""
from pignus_api.models.base import Base
from pignus_shared.utils import xlate


FIELD_MAP = [
    {
        "name": "key",
        "type": "text",
        "extra": "NOT NULL"
    },
    {
        "name": "user_id",
        "type": "int",
    },
    {
        'name': 'enabled',
        "type": "bool",
        "default": True
    },
    {
        'name': 'last_use',
        'type': 'datetime'
    },
    {
        'name': 'expiration',
        'type': 'datetime'
    },
]


class ApiKey(Base):

    model_name = "api_key"

    def __init__(self, conn=None, cursor=None):
        """Create the Api Key instance.
        :unit-test: TestApiKey::test____init__
        """
        super(ApiKey, self).__init__(conn, cursor)
        self.table_name = "api_keys"
        self.entity_name = "api_key"
        self.field_map = FIELD_MAP
        self.api_writeable_fields = ["user_id", "enabled", "expiration"]
        self.setup()

    def __repr__(self):
        """Class representation.
        :unit-test: TestApiKey::__repr__
        """
        if self.id:
            return "<ApiKey %s>" % self.id
        else:
            return "<ApiKey>"

    def get_enabled_by_key(self, key: str) -> bool:
        """"Get an ApiKey by the key if it's enabled. This is used in authentication."""
        sql = """
            SELECT *
            FROM `%(table)s`
            WHERE
                `key`="%(key)s" AND
                `enabled`=1
            LIMIT 1;
            """ % {
            "table": self.table_name,
            "key": xlate.sql_safe(key)
        }
        print(sql)
        self.cursor.execute(sql)
        raw = self.cursor.fetchone()
        if not raw:
            return False
        self.build_from_list(raw)
        return True

    def json(self) -> dict:
        """Create a JSON friendly output of the model, converting types to friendlies. This
        instance extends the Base Model's json method, removing the actual key from the normal
        response.
        """
        json_ret = super(ApiKey, self).json()
        json_ret.pop("key")
        return json_ret


# End File: pignus/src/pignus_api/models/api_key.py
