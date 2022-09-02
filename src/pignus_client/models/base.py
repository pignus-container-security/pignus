"""Pignus-Client: Model - Base

"""
from datetime import datetime

import arrow

from pignus_shared.utils import log
from pignus_shared.utils import xlate


class Base:

    def __init__(self):
        """Base client model constructor."""
        self.entity_name = None
        self.base_map = [
            {
                'name': 'id',
                'type': 'int',
                'primary': True,
            },
            {
                'name': 'created_ts',
                'type': 'datetime',
            },
            {
                'name': 'updated_ts',
                'type': 'datetime',
            }
        ]
        self.field_map = []

    def __repr__(self):
        """Base class representation"""
        return "<Base>"

    def get_by_id(self, model_id):
        self.request("/image/%s" % model_id)

    def build_from_dict(self, raw: dict) -> bool:
        """Build a model from a raw dictionary."""
        for field_name, field_value in raw.items():
            if isinstance(field_value, dict):
                continue
            if hasattr(self, field_name):
                print("setting: %s to %s" % (field_name, field_value))
                setattr(self, field_name, field_value)
        # import ipdb; ipdb.set_trace()
        return True

    def setup(self):
        """Setup the model with all class vars set and defaults applied."""
        log.info("Running Setup")
        self._create_total_map()
        self._set_defaults()
        self._set_types()

    def _create_total_map(self) -> bool:
        """Create total field map for the model.
        :unit-test: TestClientModelBase::test___create_total_map
        """
        self.total_map = self.base_map + self.field_map
        return True

    def _set_defaults(self) -> bool:
        """Set the defaults for the class field vars and populates the self.field_list var
        containing all table field names.
        :unit-test: test___set_defaults
        """
        self.field_list = []
        for field in self.total_map:
            field_name = field['name']
            self.field_list.append(field_name)

            default = None
            if 'default' in field:
                default = field['default']

            if field["type"] == "list":
                default = []

            # Sets all class field vars with defaults.
            field_value = getattr(self, field_name, None)
            if field["type"] == "bool":
                if field_value == False:
                    setattr(self, field_name, False)
                elif field_value:
                    setattr(self, field_name, True)
                else:
                    setattr(self, field_name, default)
            elif not field_value:
                setattr(self, field_name, default)

        return True

    def _set_types(self) -> bool:
        """Set the types of class table field vars and corrects their types where possible
        """
        for field in self.total_map:
            class_var_name = field['name']

            class_var_value = getattr(self, class_var_name)
            if class_var_value is None:
                continue

            if field['type'] == 'int' and type(class_var_value) != int:
                converted_value = xlate.convert_any_to_int(class_var_value)
                setattr(self, class_var_name, converted_value)
                continue

            if field['type'] == 'bool':
                converted_value = xlate.convert_int_to_bool(class_var_value)
                setattr(self, class_var_name, converted_value)
                continue

            if field['type'] == 'datetime' and type(class_var_value) != datetime:
                setattr(
                    self,
                    class_var_name,
                    arrow.get(class_var_value).datetime)
                continue

# End File: pignus/src/pignus_client/models/base.py
