"""Misc Server

"""
import codecs
import pickle
import os

from pignus_api.collects.options import Options
from pignus_api.utils import db
from pignus_api.utils import glow
from pignus_shared.utils import log


def get_option_value(option_name: str, default=None):
    """Get just the value of an Option, with an optional default if supplied."""
    option = glow.options.get(option_name)
    if not option:
        return default
    return option.value


def get_kms_key_id() -> str:
    """Get the Pignus KMS ARN from the systems environment vars."""
    kms_arn = os.environ.get("PIGNUS_AWS_KMS")
    if not kms_arn:
        log.error("Could not locate Pignus KMS ARN.")
        return False
    return kms_arn


def get_pignus_path() -> str:
    """Get the path to the Pignus repository through the PIGNUS_PATH environment var."""
    pignus_path = os.environ.get("PIGNUS_PATH")
    if not pignus_path:
        log.error("Could not determine Pignus path, please set PIGNUS_PATH enviornment var")
        return False
    return pignus_path


def get_pignus_migrations_path() -> str:
    """Get the Pignus migrations through  the PIGNUS_MIGRATIONS_PATH environment var."""
    pignus_path = os.environ.get("PIGNUS_MIGRATIONS_PATH", "/app/migrations")
    if not pignus_path:
        log.error(
            "Could not determine Pignus mgrations path, please set PIGNUS_MIGRATIONS_PATH "
            "enviornment var")
        return False
    return pignus_path


# def get_pignus_key_path() -> str:
#     """Get the name of the key path dir where the Pignus RSA key pair is stored."""
#     env_var = os.environ.get("PIGNUS_KEY_PATH")

#     if not env_var and get_pignus_path():
#         return os.path.join(get_pignus_path(), ".keys")
#     elif not env_var:
#         log.error("Could not locate Pignus KMS ARN.")
#         return False
#     else:
#         return env_var


def get_public_key_name() -> str:
    """Get the name of the SMS Parameter where the Pignus public key is stored."""
    env_var = os.environ.get("PIGNUS_PUBLIC_KEY")
    if not env_var:
        log.error("Could not locate Pignus KMS ARN.")
        return False
    return env_var


def get_private_key_name() -> str:
    """Get the name of the SMS Parameter where the Pignus private key is stored."""
    env_var = os.environ.get("PIGNUS_PRIVATE_KEY")
    if not env_var:
        log.error("Could not locate Pignus KMS ARN.")
        return False
    return env_var


def set_db():
    conn, cursor = db.connect_mysql(glow.server["DATABASE"])
    glow.db["conn"] = conn
    glow.db["cursor"] = cursor
    glow.options = Options(conn, cursor).load_options()
    return True


# def set_keys() -> bool:
#     """Collect the RSA key pair from SSM and set it in the global glow var to be used through
#     out server side applications.
#     """
#     path_key = get_pignus_key_path()
#     if not os.path.exists(path_key):
#         log.error("Pignus key path does not exist: %s" % path_key)
#         return False

#     # Get the public key
#     path_public_key = os.path.join(path_key, "id_rsa.pub")
#     if not os.path.exists(path_public_key):
#         log.error("Failed to find public key: %s" % path_public_key)
#     with open(path_public_key, "r") as phile_in:
#         phile_raw = phile_in.read()
#     public_key = pickle_out(phile_raw)

#     glow.server["KEYS"]["PUBLIC"] = public_key
#     if not isinstance(glow.server["KEYS"]["PUBLIC"], rsa.key.PublicKey):
#         log.warning("Invalid public key: %s" % glow.server["KEYS"]["PUBLIC"])

#     # Get the private key
#     path_private_key = os.path.join(path_key, "id_rsa")
#     if not os.path.exists(path_private_key):
#         log.error("Failed to find private key: %s" % path_private_key)
#     with open(path_private_key, "r") as phile_in:
#         phile_raw = phile_in.read()
#     private_key = pickle_out(phile_raw)
#     glow.server["KEYS"]["PRIVATE"] = private_key
#     if not isinstance(glow.server["KEYS"]["PRIVATE"], rsa.key.PrivateKey):
#         log.warning("Invalid private key: %s" % glow.server["KEYS"]["PRIVATE"])

#     return True


def pickle_in(data) -> str:
    """Takes a native Python object and pickles the data, then base64 encodes it to make it more
    portable.
    """
    picked_data = pickle.dumps(data)
    encoded_data = codecs.encode(picked_data, "base64").decode()
    return encoded_data


def pickle_out(data):
    """Takes input data and attemps to decode a base64 value, then load that value as a native
    Python object back out.
    @todo: Catch the exceptions better here.
    """
    if not data:
        log.warning("Cannot pickle out None")
        return None

    # Decode the value from base64
    encode_data = data.encode()
    try:
        bas64_decoded_out = codecs.decode(encode_data, 'base64')
    except Exception as e:
        log.error("Cannot pickle out: %s.\n%s" % (data, e), exception=e)
        return None

    the_object = pickle.loads(bas64_decoded_out)
    return the_object


# End File: pignus/src/pignus_api/utils/misc_server.py
