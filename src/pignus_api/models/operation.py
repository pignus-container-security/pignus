"""Operation Model
Model to keep track of CodeBuild jobs that an Image or Container is subjected to.

"""
from pignus_api.models.base import Base
from pignus_shared.utils import xlate


FIELD_MAP = [
    {
        'name': 'type',
        'type': 'str',
    },
    {
        'name': 'sub_type',
        'type': 'str',
    },
    {
        'name': 'entity_type',
        'type': 'str',
    },
    {
        "name": "entity_id",
        "type": "int",
    },
    {
        "name": "build_id",
        "type": "str",
    },
    {
        'name': 'start_ts',
        'type': 'datetime',
    },
    {
        'name': 'end_ts',
        'type': 'datetime',
    },
    {
        'name': 'result',
        'type': 'bool'
    },
    {
        'name': 'message',
        'type': 'text'
    },
]


class Operation(Base):

    model_name = "operation"

    def __init__(self, conn=None, cursor=None):
        super(Operation, self).__init__(conn, cursor)
        self.table_name = 'operations'
        self.field_map = FIELD_MAP
        self.setup()

    def __repr__(self):
        """Set the class representation
        :unit-test: TestOperation::__repr__
        """
        if self.id and self.type:
            return "<Operation %s: %s>" % (self.id, self.type)
        else:
            return "<Operation>"

    def get_by_build_id(self, build_id: str) -> bool:
        """Get an Operation from it's AWS CodeBuild build_id."""
        sql = """
            SELECT *
            FROM `operations`
            WHERE `build_id` = "%s" LIMIT 1;""" % (
            xlate.sql_safe(build_id)
        )
        self.cursor.execute(sql)
        raw = self.cursor.fetchone()
        if not raw:
            return False
        self.build_from_list(raw)
        return True

    def get_by_image_build_and_type(self, image_build_id: int, operation_type: str) -> bool:
        """Get an Operation by an ImageBuild ID and an Operation type."""
        sql = """
            SELECT *
            FROM `operations`
            WHERE
                `entity_id` = %s AND
                `type` = "%s" AND
                `entity_type` = "image_builds" AND
                `result` is NULL
            ORDER BY `id` DESC LIMIT 1;
            """ % (xlate.sql_safe(image_build_id), xlate.sql_safe(operation_type))
        self.cursor.execute(sql)
        raw = self.cursor.fetchone()
        if not raw:
            return False
        self.build_from_list(raw)
        return True

# End File: pignus/src/pignus_api/modles/operation.py
