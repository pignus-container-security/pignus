"""Role Perm Model
Binds the Role and Perm models to create a role level understanding of Role's access to Permissions

"""
from pignus_api.models.base import Base
from pignus_shared.utils import xlate

FIELD_MAP = [
    {
        "name": "role_id",
        "type": "int",
    },
    {
        "name": "perm_id",
        "type": "int",
    },
    {
        "name": "enabled",
        "type": "bool",
        "default": True
    }

]


class RolePerm(Base):

    model_name = "role_perm"

    def __init__(self, conn=None, cursor=None):
        super(RolePerm, self).__init__(conn, cursor)
        self.table_name = "role_perms"
        self.field_map = FIELD_MAP
        self.setup()

    def __repr__(self):
        if self.id:
            return "<RolePerm %s:(Role.ID %s, Perm.ID %s)>" % (self.id, self.role_id, self.perm_id)
        else:
            return "<RolePerm %s>" % (self.id)

    def get_by_role_perm(self, role_id: int, perm_id) -> bool:
        sql = """
            SELECT *
            FROM `role_perms`
            WHERE
                `role_id` = %s AND
                `perm_id` = %s AND
                `enabled` = 1
            LIMIT 1; """ % (xlate.sql_safe(role_id), xlate.sql_safe(perm_id))
        self.cursor.execute(sql)
        raw = self.cursor.fetchone()
        if not raw:
            return False
        self.build_from_list(raw)
        return True


# End File: pignus/src/pignus_api/models/role_perm.py
