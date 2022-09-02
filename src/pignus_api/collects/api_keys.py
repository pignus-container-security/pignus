"""ApiKeys Collection

"""
from pignus_api.collects.base import Base
from pignus_api.models.api_key import ApiKey
from pignus_shared.utils import xlate


class ApiKeys(Base):

    collection_name = "api_keys"

    def __init__(self, conn=None, cursor=None):
        """ApiKeys Collection"""
        super(ApiKeys, self).__init__(conn, cursor)
        self.table_name = "api_keys"
        self.collect_model = ApiKey

    def get_api_keys_for_user(self, user_id: int) -> list:
        """Get all the ApiKeys for a User by ID."""
        sql = """
            SELECT *
            FROM `api_keys`
            WHERE
                `user_id` = %s AND
                `enabled` = 1;
            """ % xlate.sql_safe(user_id)
        self.cursor.execute(sql)
        raws = self.cursor.fetchall()
        prestines = self.build_from_lists(raws)
        return prestines

    def get_all_enabled(self) -> bool:
        """
        """
        sql = """
            SELECT *
            FROM `api_keys`
            WHERE `enabled` = 1;
            """
        self.cursor.execute(sql)
        raws = self.cursor.fetchall()
        prestines = self.build_from_lists(raws)
        return prestines

    def disable_all(self) -> bool:
        """Disable all current ApiKeys."""
        all_keys = self.get_all()
        for key in all_keys:
            key.enabled = False
            key.save()
        return True

# End File: pigns/src/pignus_api/collects/api_keys.py
