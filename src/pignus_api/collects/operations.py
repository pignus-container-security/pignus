"""Operations Collection

"""
from pignus_api.collects.base import Base
from pignus_api.models.operation import Operation


class Operations(Base):
    def __init__(self, conn=None, cursor=None):
        super(Operations, self).__init__(conn, cursor)
        self.table_name = Operation().table_name
        self.collect_model = Operation

    def get_by_image_id(self, image_id: int) -> list:
        """Get Operations for a given Image ID."""
        args = {
            "image_id": image_id
        }
        sql = """
            SELECT *
            FROM `operations`
            WHERE
                `entity_id` = %(image_id)s AND
                `entity_type` = "images"
            ORDER BY `updated_ts` DESC;"""
        self.cursor.execute(sql, args)
        raws = self.cursor.fetchall()
        prestines = self.build_from_lists(raws)
        return prestines

    def get_by_image_build_id(self, image_build_id: int) -> list:
        """Get Operations for a given Container ID."""
        args = {
            "image_build_id": image_build_id
        }
        sql = """
            SELECT *
            FROM `operations`
            WHERE
                `entity_id` = %(image_build_id)s AND
                `entity_type` = "image_builds"
            ORDER BY `updated_ts` DESC;"""
        self.cursor.execute(sql, args)
        raws = self.cursor.fetchall()
        prestines = self.build_from_lists(raws)
        return prestines

    def get_pending_scans_by_build_id(self, image_build_id: int) -> list:
        """Get pending Operations for a given ImageBuild ID."""
        args = {
            "image_build_id": image_build_id
        }
        sql = """
            SELECT *
            FROM `operations`
            WHERE
                `entity_id` = %(image_build_id)s AND
                `end_ts` IS NULL AND
                `type` = "scan" AND
                `entity_type` = "image_builds"
            ORDER BY `updated_ts` DESC;"""
        self.cursor.execute(sql, args)
        raws = self.cursor.fetchall()
        prestines = self.build_from_lists(raws)
        return prestines

    def get_pending_by_build_id(self, image_build_id: int) -> list:
        """Get pending Operations for a given ImageBuild ID."""
        args = {
            "image_build_id": image_build_id
        }
        sql = """
            SELECT *
            FROM `operations`
            WHERE
                `entity_id` = %(image_build_id)s AND
                `end_ts` IS NULL AND
                `entity_type` = "image_builds"
            ORDER BY `updated_ts` DESC;"""
        self.cursor.execute(sql, args)
        raws = self.cursor.fetchall()
        prestines = self.build_from_lists(raws)
        return prestines

# End File: pignus/src/pignus_api/collections/operations.py
