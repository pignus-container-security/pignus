"""Scans Collection

"""
from pignus_api.collects.base_entity_metas import BaseEntityMetas
from pignus_api.models.scan import Scan
from pignus_shared.utils import xlate


class Scans(BaseEntityMetas):
    def __init__(self, conn=None, cursor=None):
        """Scans Collection"""
        super(Scans, self).__init__(conn, cursor)
        self.table_name = "scans"
        self.collect_model = Scan

    def get_by_image_id(self, image_id: int) -> list:
        """Get all Scans for a given Image ID."""
        sql = """
            SELECT *
            FROM `scans`
            WHERE `image_id` = %s;""" % xlate.sql_safe(image_id)
        self.cursor.execute(sql)
        raws = self.cursor.fetchall()
        prestines = self.build_from_lists(raws)
        return prestines

    def get_last(self, image_build_id: int, scanner_id: int) -> Scan:
        """Get the last Scan for an ImageBuild with with a given ImageBuild ID and Scanner ID. """
        sql = """
            SELECT *
            FROM `scans`
            WHERE
                `image_build_id` = %s AND
                `scanner_id` = %s
            ORDER BY `id` DESC
            LIMIT 1;""" % (
            xlate.sql_safe(image_build_id),
            xlate.sql_safe(scanner_id),
        )
        self.cursor.execute(sql)
        raws = self.cursor.fetchall()
        if not raws:
            return None
        prestines = self.build_from_lists(raws)
        return prestines[0]

    def get_by_image_build_id(self, image_build_id: int, scanner_ids: list = []) -> list:
        """Get all Scans for a given ImageBuild ID."""
        scanner_sql = ""
        limit_sql = 1
        if scanner_ids:
            scanner_ids_sql = xlate.comma_separate_list(scanner_ids)
            scanner_sql = " AND scanner_id IN(%s)" % scanner_ids_sql
            limit_sql = len(scanner_ids)
        sql = """
            SELECT *
            FROM `scans`
            WHERE `image_build_id` = %s %s
            ORDER BY `id` DESC
            LIMIT %s;""" % (
            xlate.sql_safe(image_build_id),
            scanner_sql,
            limit_sql
        )
        self.cursor.execute(sql)
        raws = self.cursor.fetchall()
        prestines = self.build_from_lists(raws)
        return prestines

    def find_cve(self, cve_number: str):
        """
        CVE-2021-3121
        """
        sql = """
            SELECT *
            FROM `scans`
            WHERE
                `cve_critical_nums` LIKE "%%%(cve_number)s%%" OR
                `cve_high_nums` LIKE "%%%(cve_number)s%%" OR
                `cve_medium_nums` LIKE "%%%(cve_number)s%%" OR
                `cve_low_nums` LIKE "%%%(cve_number)s%%";
        """ % {
            "cve_number": xlate.sql_safe(cve_number)
        }
        self.cursor.execute(sql)
        raws = self.cursor.fetchall()
        prestines = self.build_from_lists(raws)
        return prestines


# End File: pignus/src/pignus_api/collections/scans.py
