"""Entity Meta Model

How to use:
    The Device model is a good example to follow.

    To give a model the ability to use EntityMetas the class must:
        - extend the BaseEntityMeta
        - define a `self.metas = {}` in the init

    To set a new EntityMeta value for an object which may or may not have the EntityMeta yet.

        if 'notes' not in device.metas:
            # Create the notes meta if it doesn't exist
            device.metas['notes'] = EntityMeta()
            device.metas['notes'].create(
                meta_name='notes',
                meta_type='str',
                meta_value=device_notes)
        else:
            # Update the device notes.
            device.metas['notes'].value = request.form['device_notes']

"""
from pignus_api.models.base import Base
from pignus_api.utils import date_utils
from pignus_shared.utils import xlate


class EntityMeta(Base):

    def __init__(self, conn=None, cursor=None):
        super(EntityMeta, self).__init__(conn, cursor)

        self.table_name = 'entity_metas'
        self.field_map = [
            {
                'name': 'entity_type',
                'type': 'str',
            },
            {
                'name': 'entity_id',
                'type': 'int',
            },
            {
                'name': 'name',
                'type': 'str',
            },
            {
                'name': 'type',
                'type': 'str'
            },
            {
                'name': 'value',
                'type': 'str'
            },
        ]
        self.setup()

    def __repr__(self):
        """Set the class representation
        :unit-test: TestEntityMeta::__repr__
        """
        if self.entity_type and self.name:
            return "<EntityMeta %s %s:%s>" % (self.entity_type, self.name, self.value)
        return "<EntityMeta>"

    def build_from_list(self, raw: list):
        """Build a model from an ordered list, converting data types to their desired type where
        possible.
        """
        count = 0
        for field in self.total_map:
            setattr(self, field['name'], raw[count])
            count += 1
            if self.type == 'bool':
                self.value = xlate.convert_int_to_bool(self.value)

        return True

    def create(
        self,
        meta_name: str,
        meta_type: str,
        entity_id: int,
        meta_value: str = None
    ) -> bool:
        """Initiate a new EntityMeta object with a name, type and optional value.

        :param meta_name: The meta key name for the entity meta.
        :param meta_type: The meta's data type. Supported str, int and bool currently.
        :param meta_value: The value to set for the meta.
        """
        self.name = meta_name
        self.type = meta_type
        self.entity_id = entity_id
        self.value = meta_value
        self.entity_type = self.table_name

        # Validate the data type for the entity meta
        if self.type not in ['str', 'int', 'bool']:
            raise AttributeError('Invalid EntityMeta type: %s' % self.type)

        # Validate the entity_type, which requires the model to set the `self.table_name` var.
        if not self.entity_type:
            raise AttributeError(
                "Invalid EntityType type: %s, must set model's self.table_name" % self.entity_type)

        return True

    def json(self) -> dict:
        """Create a JSON friendly output of the model, converting types to friendlies. This
        instance extends the Base Model's json method and adds "clusters" to the output.
        """
        json_ret = {
            "created_ts": date_utils.json_date(self.created_ts),
            "updated_ts": date_utils.json_date(self.updated_ts),
            "name": self.name,
            "type": self.type,
            "value": self.value
        }
        return json_ret

# End File: pignus/src/pignus_api/models/entity_meta.py
