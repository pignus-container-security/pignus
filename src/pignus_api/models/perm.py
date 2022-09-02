"""Perm Model

"""
from pignus_api.models.base import Base
from pignus_shared.utils import xlate


FIELD_MAP = [
    {
        "name": "name",
        "type": "str",
    },
    {
        "name": "slug_name",
        "type": "str",
    }
]


class Perm(Base):

    model_name = "perm"

    def __init__(self, conn=None, cursor=None):
        super(Perm, self).__init__(conn, cursor)
        self.table_name = "perms"
        self.field_map = FIELD_MAP
        self.setup()

    def __repr__(self):
        if self.id:
            return "<Perm %s:%s>" % (self.id, self.slug_name)
        else:
            return "<Perm>"

    def get_by_slug(self, slug_name: str) -> bool:
        sql = """
            SELECT *
            FROM `perms`
            WHERE
                `slug_name` = "%s"
            LIMIT 1; """ % xlate.sql_safe(slug_name)
        self.cursor.execute(sql)
        raw = self.cursor.fetchone()
        if not raw:
            return False
        self.build_from_list(raw)
        return True

# End File: pignus/src/pignus_api/models/perm.py
