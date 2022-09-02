"""Collection - Users

"""
from pignus_api.collects.base_entity_metas import BaseEntityMetas
from pignus_api.models.user import User


class Users(BaseEntityMetas):

    collection_name = "users"

    def __init__(self, conn=None, cursor=None):
        super(Users, self).__init__()
        self.table_name = User().table_name
        self.collect_model = User
        self.order_by = {
            "field": "last_login",
            "op": "DESC"
        }

# End File: pignus/src/pignus_api/collects/users.py
