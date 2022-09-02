#!/usr/bin/env python


from pignus_api.models.user import User
from pignus_api.models.api_key import ApiKey
from pignus_api.models.option import Option
from pignus_api.utils import glow
from pignus_api.utils import db
from pignus_api.utils import auth
from pignus_shared.utils import log


def create_user():
    user = User()
    user.name = "pignus-admin"
    user.client_id = auth.generate_client_id()
    user.role_id = 1
    user.save()

    api_key = ApiKey()
    api_key.user_id = user.id
    key = auth.generate_api_key()
    api_key.key = auth.generate_password_hash(key)
    api_key.save()

    log.info("Created User: %s Client ID: %s ApiKey: %s" % (
        user.name,
        user.client_id,
        key)
    )


def create_option_defaults():
    # option = Option()
    # option.name = "DEFAULT_SCANNER"
    # option.type = "str"
    # option.value = 1
    # option.save()
    option = Option()
    option.name = "TRIVY_VERSION"
    option.type = "str"
    option.value = "aquasec/trivy:0.18.3"
    option.save()
    log.info("Created option: %s" % option)


if __name__ == "__main__":
    glow.db = db.connect()
    create_option_defaults()
    # create_user()


# End File: pignus/src/pignus_api/migrate.py
