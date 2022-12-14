"""Scanner Model

"""
from pignus_api.models.base_entity_meta import BaseEntityMeta


FIELD_MAP = [
    {
        'name': 'name',
        'type': 'str',
    },
    {
        'name': 'build_name',
        'type': 'str',
    },
    {
        "name": "parser_name",
        "type": "str",
    },
    {
        "name": "enabled",
        "type": "bool",
        "default": True,
    }
]


class Scanner(BaseEntityMeta):

    model_name = "scanner"

    def __init__(self, conn=None, cursor=None):
        super(Scanner, self).__init__(conn, cursor)
        self.table_name = 'scanners'
        self.field_map = FIELD_MAP
        self.metas = {}
        self.setup()

    def __repr__(self):
        if self.id:
            return "<Scanner %s: %s>" % (self.id, self.name)
        else:
            return "<Scanner>"

# End File: pignus/src/pignus_api/models/scanner.py
