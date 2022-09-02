"""Role Model

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


class Role(Base):

    model_name = "role"

    def __init__(self, conn=None, cursor=None):
        super(Role, self).__init__(conn, cursor)
        self.table_name = "roles"
        self.field_map = FIELD_MAP
        self.setup()

    def __repr__(self):
        if self.id:
            return "<Role %s:%s>" % (self.id, self.slug_name)
        else:
            return "<Role %s>" % (self.slug_name)

    def get_by_slug(self, slug_name: str) -> bool:
        sql = """
            SELECT *
            FROM `roles`
            WHERE
                `slug_name` = "%s"
            LIMIT 1; """ % xlate.sql_safe(slug_name)
        self.cursor.execute(sql)
        raw = self.cursor.fetchone()
        if not raw:
            return False
        self.build_from_list(raw)
        return True

# End File: pignus/src/pignus_api/models/role.py
