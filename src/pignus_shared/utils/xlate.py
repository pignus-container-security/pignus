"""Utility Xlate
A collection of misc trasnlation functions used all throuhout the Pignus platofrm.

"""
from datetime import datetime
import json
from urllib.parse import unquote, quote

from sqlescapy import sqlescape

from pignus_shared.utils import log


def url_decode(encoded_str: str) -> str:
    """Decode a URL str such as "haproxy%3A2.0.12" to "haproxy/2.0.12"
    :unit-test: TestXlate::test__url_decode
    """
    if not encoded_str:
        return ""
    return unquote(encoded_str)


def url_encode(slug: str) -> str:
    """Encode a str to be URL safe. Such as "haproxy:2.0.12" to "haproxy%3A2.0.12"
    :unit-test: TestXlate::test__url_encode
    """
    butterfly = quote(slug)
    butterfly = butterfly.replace("/", "%2F")
    return butterfly


def decode_post_data(post_data: str) -> dict:
    """Take post data from a POST request and separate it into a key value dictionary.
    :unit-test: TestXlate::test__decode_post_data
    """
    try:
        data = json.loads(post_data)
        return data
    except json.decoder.JSONDecodeError as e:
        log.warning("Failed parsing decode post data: %s" % post_data, exception=e)
        raise e


def convert_any_to_int(value) -> int:
    """Attempt to convert any value into an int
    :unit-test: TestXlate::test__convert_any_to_int
    """
    if not value:
        return None
    elif isinstance(value, float):
        return int(value)
    elif isinstance(value, int):
        return value
    else:
        try:
            if value.isdigit():
                return int(value)
            else:
                raise AttributeError(
                    'Cannot convert "%s" of type "%s" to int.' % (
                        value,
                        type(value)))
        except AttributeError as e:
            raise AttributeError(
                'Cannot convert "%s" of type "%s" to int. Exception: %s' % (
                    value,
                    type(value),
                    e))


def convert_bool_to_int(value: bool) -> int:
    """Convert a bool into an int. Typically used for storing bools as TINYINT in SQL.
    :unit-test: TestXlate::test__convert_bool_to_int
    """
    if isinstance(value, type(None)):
        return None
    elif value:
        return 1
    elif not value:
        return 0
    else:
        msg = 'Cannot convert "%s" of type "%s" to int' % (value, type(value))
        raise AttributeError(msg)


def convert_int_to_bool(value: int) -> bool:
    """Convert an into into a bool. Typically used for pulling TINYINT values out of a SQL
    database and converting it into a python bool
    :unit-test: TestXlate::test__convert_int_to_bool
    """
    if isinstance(value, type(None)):
        return None
    elif value == 1:
        return True
    elif value == 0:
        return False


def convert_list_to_str(value: list) -> str:
    """Convert a list into a str. Typically used for storing lists as a TEXT field in SQL.
    :unit-test: TestXlate::test__convert_bool_to_int
    """
    if not value:
        return None
    if not isinstance(value, list):
        msg = "Cannot convert list to str: %s" % value
        raise AttributeError(msg)

    clean_values = []
    for item in value:
        clean_values.append(str(item))

    return ",".join(clean_values)


def convert_any_to_native(value: str):
    """Convert a value to its native Python type, such as a string "true" to a bool True.
    :unit-test: TestXlate::test__convert_any_to_native
    """
    if not value:
        return None

    if isinstance(value, str):
        if value.lower() == "true":
            return True
        elif value.lower() == "false":
            return False

    return value


def convert_str_to_bool(value: str) -> bool:
    """Convert a string value to a bool value if one can be derrived.
    :unit-test: TestXlate::test__convert_str_to_bool
    """
    if not value:
        return None
    if isinstance(value, bool):
        return value
    value = value.lower().strip()
    accepted_true_values = ["true", "1"]
    accepted_false_values = ["false", "0"]

    if value in accepted_true_values:
        return True
    elif value in accepted_false_values:
        return False
    return None


def sql_safe(query_item):
    """Covert any item to a sql safe value where possible.
    :unit-test: TestXlate::test__sql_safe
    """
    if not query_item:
        return query_item
    if isinstance(query_item, str) and query_item.isdigit():
        return query_item
    elif isinstance(query_item, datetime):
        return query_item
    elif isinstance(query_item, int):
        return query_item
    elif isinstance(query_item, dict):
        log.error("sql_safe cannot translate dict objects")
        raise AttributeError("sql_safe cannot translate dict objects")
    else:
        return sqlescape(query_item)


def aws_account_docker_url(docker_url: str) -> str:
    """Get the AWS account number from a docker url if one exists.
    :unit-test: TestXlate::test__aws_account_docker_url
    """
    if "dkr.ecr." not in docker_url:
        return ""
    else:
        return docker_url[:docker_url.find(".")]


def get_digest(image_str: str):
    """Extracts the digest from a docer-pullable string as given from the K8 api
    example image_str: docker-pullable://docker.io/politeauthority/pignus@sha256:\
        d480d804f0c11548d6be95568
    :unit-test: TestXlate::test__get_digest
    """
    return image_str[image_str.find("@sha256:") + 8:]


def json_dump(the_dict: dict) -> str:
    """Create a JSON safe str from native Python objects, recursively iterating over a dictionary
    and converting those that would normally break into their str representation.
    :unit-test: TestXlate::test__json_dump()
    """
    new_json = _convert_dict_objects(the_dict)
    return json.dumps(new_json)


def _convert_dict_objects(the_dict):
    """Recursily scrubs non serializable objects from a dictionary replacing them with their str
    represntations.
    :unit-test: TestXlate::_convert_dict_objects()
    """
    new_dict = {}
    for key, value in the_dict.items():
        if _is_jsonable(value, exclude_dicts=True):
            new_dict[key] = value
        elif isinstance(value, dict):
            new_dict[key] = _convert_dict_objects(value)
        else:
            new_dict[key] = str(value)
    return new_dict


def _is_jsonable(item, exclude_dicts: bool = False) -> bool:
    """Tests to see if a given value is JSONable.
    :unit-test: TestXlate::test___is_jsonable()
    """
    jsonable = ["str", "bool", "int", "float"]
    if not exclude_dicts:
        jsonable.append("dict")
    if type(item).__name__ in jsonable:
        return True
    else:
        return False


def comma_separate_list(the_list: list) -> str:
    """
    """
    ret_string = ""
    for item in the_list:
        ret_string += "%s," % str(item)
    if ret_string:
        ret_string = ret_string[:-1]
    return ret_string

# End File: pignus/src/pignus_shared/utils/xlate.py
