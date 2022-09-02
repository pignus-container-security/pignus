"""Pignus-Shared: Model - Image Build

"""

FIELD_MAP = [
    {
        "name": "digest",
        "type": "str",
        "extra": "UNIQUE"
    },
    {
        "name": "digest_local",
        "type": "str",
    },
    {
        "name": "image_id",
        "type": "int",
        "extra": "NOT NULL"
    },
    {
        "name": "repository",
        "type": "str",
        "extra": "NOT NULL"
    },
    {
        "name": "tags",
        "type": "list"
    },
    {
        "name": "maintained",
        "type": "bool",
        "default": True
    },
    {
        "name": "state",
        "type": "str"
    },
    {
        "name": "state_msg",
        "type": "str"
    },
    {
        "name": "sync_flag",
        "type": "bool"
    },
    {
        "name": "sync_enabled",
        "type": "bool",
        "default": True,
    },
    {
        "name": "sync_last_ts",
        "type": "datetime",
    },
    {
        "name": "scan_flag",
        "type": "bool"
    },
    {
        "name": "scan_enabled",
        "type": "bool",
        "default": True,
    },
    {
        "name": "scan_last_ts",
        "type": "datetime",
    },
    {
        "name": "pending_operation",
        "type": "str",
    },
]

# End File: pignus/src/pignus_shared/models/image_build.py
