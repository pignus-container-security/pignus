"""Migration Model
Model used for tracting Pignus database migrations

"""
from pignus_api.models.base import Base


FIELD_MAP = [
    {
        'name': 'number',
        'type': 'int',
    },
    {
        "name": "pignus_version",
        "type": "str",
    },
    {
        "name": "notes",
        "type": "text",
    },
    {
        "name": "status",
        "type": "bool",
    },
]


class Migration(Base):

    model_name = "migration"

    def __init__(self, conn=None, cursor=None):
        """Create the Cluster instance.
        :unit-test: TestCluster::test____init__
        """
        super(Migration, self).__init__(conn, cursor)
        self.table_name = "migrations"
        self.field_map = FIELD_MAP
        self.setup()

    def __repr__(self):
        """Class representation.
        :unit-test: Migration::__repr__
        """
        if self.id:
            return "<Migration %s>" % self.number
        else:
            return "<Migration>"


# End File: pignus/src/pignus_api/models/migration.py
