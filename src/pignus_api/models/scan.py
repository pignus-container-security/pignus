"""Scan Model

"""
from pignus_api.models.base_entity_meta import BaseEntityMeta
from pignus_shared.utils import xlate


FIELD_MAP = [
    {
        "name": "image_id",
        "type": "int",
    },
    {
        "name": "image_build_id",
        "type": "int"
    },
    {
        "name": "scanner_id",
        "type": "int",
    },
    {
        "name": "operation_id",
        "type": "int"
    },
    {
        "name": "codebuild_id",
        "type": "str"
    },
    {
        "name": "ended_ts",
        "type": "datetime",
    },
    {
        "name": "scan_job_success",
        "type": "bool"
    },
    {
        "name": "scan_score",
        "type": "bool"
    },
    {
        "name": "cve_critical_int",
        "type": "int",
        "default": 0
    },
    {
        "name": "cve_critical_nums",
        "type": "list"
    },
    {
        "name": "cve_high_int",
        "type": "int",
        "default": 0
    },
    {
        "name": "cve_high_nums",
        "type": "list"
    },
    {
        "name": "cve_medium_int",
        "type": "int",
        "default": 0
    },
    {
        "name": "cve_medium_nums",
        "type": "list"
    },
    {
        "name": "cve_low_int",
        "type": "int",
        "default": 0
    },
    {
        "name": "cve_low_nums",
        "type": "list"
    },
    {
        "name": "cve_unknown_int",
        "type": "int",
        "default": 0
    },
    {
        "name": "cve_unknown_nums",
        "type": "list"
    },
]


class Scan(BaseEntityMeta):

    model_name = "scan"

    def __init__(self, conn=None, cursor=None):
        super(Scan, self).__init__(conn, cursor)
        self.table_name = "scans"
        self.metas = {}
        self.field_map = FIELD_MAP
        self.setup()

    def __repr__(self):
        """Set the class representation
        :unit-test: TestScan::__repr__
        """
        return "<Scan>"

    def save(self) -> int:
        """Save a Scan record, totaling up the number of CVEs at each severity automatically prior
        to save.
        """
        self.cve_critical_int = len(self.cve_critical_nums)
        self.cve_high_int = len(self.cve_high_nums)
        self.cve_medium_int = len(self.cve_medium_nums)
        self.cve_low_int = len(self.cve_low_nums)
        return super(Scan, self).save()

    def get_build_last(self, image_build_id: int, scanner_id=None) -> bool:
        """Get the last Scan for container. """
        if not scanner_id:
            scanner_id = 1
        sql = """
            SELECT *
            FROM `scans`
            WHERE
                `image_build_id` = %(image_build_id)s  AND
                `scanner_id` = %(scanner_id)s
            ORDER BY `end_ts` DESC
            LIMIT 1;
        """ % {
            "image_build_id": xlate.sql_safe(image_build_id),
            "scanner_id": xlate.sql_safe(scanner_id),
        }
        self.cursor.execute(sql)
        raw = self.cursor.fetchone()
        if not raw:
            return False
        self.build_from_list(raw)
        return True

    def get_by_codebuild_id(self, codebuild_id: int = None) -> bool:
        if not codebuild_id:
            codebuild_id = self.codebuild_id
        sql = """
            SELECT *
            FROM `scans`
            WHERE `codebuild_id` = "%s";
        """ % xlate.sql_safe(codebuild_id)
        self.cursor.execute(sql)
        raw = self.cursor.fetchone()
        if not raw:
            return False
        self.build_from_list(raw)
        return True


# End File: pignus/src/pignus_api/modles/scan.py
