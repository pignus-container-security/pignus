"""Pignus-Shared: Model - Image Build

"""

FIELD_MAP = [
    {
        'name': 'name',
        'type': 'str',
        "extra": "UNIQUE"
    },
    {
        "name": "repositories",
        "type": "list",
        "extra": "NOT NULL"
    },
    {
        'name': 'maintained',
        "type": "bool",
        "default": True
    },
    {
        'name': 'state',
        'type': 'str'
    },
    {
        'name': 'state_msg',
        'type': 'str'
    },
]

# End File: pignus/src/pignus_shared/models/image.py
