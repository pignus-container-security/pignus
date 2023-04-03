"""Option Model

"""
from pignus_api.models.base import Base


class Option(Base):

    model_name = "option"

    def __init__(self, conn=None, cursor=None):
        super(Option, self).__init__(conn, cursor)
        self.table_name = 'options'
        self.field_map = [
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
        if self.name:
            return "<Option %s:%s>" % (self.name, self.value)
        else:
            return "<Option>"

    def get_by_name(self, name: str = None) -> bool:
        """Get an option from the options table based on name. """
        if not name:
            name = self.name
        if not name:
            raise ValueError('Missing name class var and method argument.')

        sql = """SELECT * FROM options WHERE name='%s'""" % name
        self.cursor.execute(sql)
        option_raw = self.cursor.fetchone()
        if not option_raw:
            return False

        self.build_from_list(option_raw)

        return True

    def build_from_list(self, raw: list):
        """Build a model from an ordered list, converting data types to their desired type where
        possible.
        """
        count = 0
        for field in self.total_map:
            setattr(self, field['name'], raw[count])
            count += 1

            if not self.value:
                continue

            # Handle bool type Options
            if self.type == 'bool':
                self.value = self._set_bool(self.value)

            # Handle list type Options
            elif self.type == "list":
                if self.value and "," not in self.value:
                    self.value = [self.value]
                elif not self.value:
                    self.value = []
                elif "," in self.value:
                    self.value = self.value.split(",")
                else:
                    self.value = []

            # Handle bool type Options
            if self.type == 'int':
                if not self.value.isdigit():
                    self.value = None
                else:
                    self.value = int(self.value)

        return True

    def update(self):
        """Save an option with Option types preserved."""
        if self.type == 'bool':
            if self.value == 'true':
                self.value = 1
            elif self.value == 'false':
                self.value = 0
        return self.save()

    def set_default(self, the_option: dict) -> bool:
        """Set a default value for an option, if the option is already set, return False otherwise
        return True
        """
        option_name = the_option['name']
        self.get_by_name(option_name)
        if self.name:
            return False
        self.name = option_name
        self.type = the_option['type']
        if 'default' in the_option:
            self.value = the_option['default']
        self.save()
        return True

    def _set_bool(self, value) -> bool:
        """Set a boolean option to the correct value. """
        value = str(value).lower()
        # Try to convert values to the positive.
        if value == '1' or value == 'true':
            return True
        # Try to convert values to the negative.
        elif value == '0' or value == 'false':
            return False

    def sql_value_override_for_model(self, field: dict) -> str:
        """Override the SQL value for a field before it's stored into the database."""
        val = getattr(self, field["name"])
        if self.type == "list" and field["name"] == "value":
            if not val:
                return None
            elif isinstance(val, list):
                return ",".join(val)
        else:
            return val

# End File: pignus/src/pignus_api/models/option.py
