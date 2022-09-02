"""Misc
A collection of miscellaneous functions with no better place to go.

"""
import importlib
import pprint
import random
import re
import string

import glom
import validators


def parse_image_url(image_str: str, set_defaults=True) -> dict:
    default_docker_repository = "docker.io/"
    default_image_tag = "latest"
    ret = {
        "repository": "",
        "repository_origin": "",
        "name": "",
        "tag": "",
        "full": "",
        "ecr_source": False,
        "digest": "",
    }
    # If the repository is present in the image url we'll use it, if not assume it's the default
    # registry

    if "/" in image_str:
        first_segment = image_str[: image_str.find("/")]
        if validators.domain(first_segment):
            ret["repository"] = first_segment
            ret["name"] = image_str[image_str.find("/") + 1:]
        else:
            ret["name"] = image_str
    else:
        ret["name"] = image_str

    ret["name"] = ret["name"].replace("//", "/")

    if set_defaults:
        if not ret["repository"]:
            ret["repository"] = default_docker_repository

    # Make sure repository doesn't end with slash.
    if ret["repository"][-1:] == "/":
        ret["repository"] = ret["repository"][:-1]

    if ret["name"][0] == "/":
        ret["name"] = ret["name"][1:]

    if "@sha256:" in ret["name"]:
        ret["digest"] = ret["name"][ret["name"].find("@sha256:") + 8:]
        ret["name"] = ret["name"][: ret["name"].find("@sha256:")]

    # Find the image tag, if one does not exist, set to "latest" unless we have a digest
    if image_str.count(":") == 2:
        ret["tag"] = image_str[image_str.find(":") + 1: image_str.rfind(":") - 7]
    elif image_str.count(":") == 1:
        if "@sha256:" in image_str:
            ret["tag"] = ""
        else:
            ret["tag"] = image_str[image_str.find(":") + 1:]
    elif set_defaults:
        ret["tag"] = default_image_tag

    if ":" in ret["name"]:
        ret["name"] = ret["name"][: ret["name"].find(":")]

    # Create the "full" representation of a image url.
    if ret["digest"] and ret["tag"]:
        ret["full"] = "%s/%s:%s@sha256:%s" % (
            ret["repository"],
            ret["name"],
            ret["tag"],
            ret["digest"],
        )
    elif ret["digest"]:
        ret["full"] = "%s/%s@sha256:%s" % (
            ret["repository"],
            ret["name"],
            ret["digest"],
        )
    else:
        ret["full"] = "%s/%s:%s" % (ret["repository"], ret["name"], ret["tag"])

    if not set_defaults:
        ret["full"] = image_str
    ret["full"] = ret["full"].replace("//", "/")
    ret["repo_image"] = "%s" % ret["name"].replace(default_docker_repository, "")
    ret["ecr_source"] = is_ecr_url(ret["full"])

    ret["repository_origin"] = ret["repository"]

    return ret


def parse_image_dir(image_name: str) -> dict:
    """Parse an image name like "secops/new", breaking it into it's repo_base
    "something/secops", and the sub_image "new"
    :unit-test: TestMisc.test__parse_image_dir
    """
    image_repo = image_name.split("/")
    repo_base = ""
    sub_image = ""
    if len(image_repo) == 1:
        repo_base = image_repo[0]
        sub_image = image_repo[0]
    elif len(image_repo) == 2:
        repo_base = image_repo[0]
        sub_image = image_repo[1]
    elif len(image_repo) >= 3:
        repo_base = image_repo[0]
        sub_image = "/".join(image_repo[1:])
    return {
        "repo_base": repo_base,
        "sub_image": sub_image
    }


def is_ecr_url(image: str) -> bool:
    """Checks if an image url is from our private ECR.
    :unit-test: TestMisc.test__is_ecr_url
    """
    if ".dkr.ecr.us-west-2.amazonaws.com" in image:
        return True
    return False


def get_origin_aws_account(image_url: str) -> str:
    """Get the AWS account number for an images original repository.
    :unit-test: TestMisc.test__get_origin_aws_account
    """
    if "dkr.ecr.us-west-2.amazonaws.com" not in image_url:
        return ""
    else:
        return image_url[: image_url.find(".dkr.ecr.us-west-2.amazonaws.com")]


# Even more miscellaneous functions
def get_supported_scans() -> list:
    """Get the supported scans from the environment var as a list.
    :unit-test: TestMisc.test__get_supported_scans
    """
    # return _get_env_as_list(os.environ.get('PIGNUS_SUPPORTED_SCANS', ''))
    return ["crowdstrike"]


def _get_env_as_list(env_var: str) -> list:
    """Get an environment variable as a list.
    :unit-test: TestMisc.test___get_env_as_list
    """
    env_var = env_var.replace(" ", "")
    if "," in env_var:
        list_env = env_var.split(",")
    elif not env_var:
        list_env = []
    else:
        list_env = [env_var]
    return list_env


def pretty_print(data) -> bool:
    """Pretty print any given data.
    :unit-test: TestMisc.test__pretty_print
    """
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(data)
    return True


def pp(data):
    """Alias for pretty_print()"""
    return pretty_print(data)


def try_path(element: dict, path: str):
    """Checks to see if a path exists in a nested dict, returning the value if it does, or None if
    it does not.
    :unit-test: TestMisc.test__try_path
    """
    try:
        return glom.glom(element, path)
    except glom.core.PathAccessError:
        return False


def generate_random_digest() -> str:
    """Generates a random docker digest sha to use for testing.
    :unit-test: TestMisc.test__generate_random_digest
    """
    numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    random_digest = "fakedigest"
    while len(random_digest) != 64:
        # 56% of chars appear to be numbers
        if random.randint(1, 100) > 56:
            random_digest += str(numbers[random.randint(0, 9)])
        else:
            random_digest += string.ascii_lowercase[random.randint(0, 25)]
    return random_digest


def compile_iam_statements(existing_statemnt: dict, new_statement: dict) -> dict:
    """Takes existing an IAM statement and new statement and melds them into one. Not including the
    new statement if it's SID matches.
    :unit-test: TestMisc::test__compile_iam_statements
    """
    for statement in existing_statemnt["Statement"]:
        if new_statement["Statement"][0]["Sid"] == statement["Sid"]:
            return existing_statemnt

    combind_statements = existing_statemnt
    combind_statements["Statement"].append(new_statement["Statement"][0])
    return combind_statements


def strip_trailing_slash(url: str) -> str:
    """Removing trailing slashes from a url if they exist.
    :unit-test: TestMisc::test__strip_trailing_slash
    """
    if not url:
        return ""
    url = url.lower()
    url = url.replace("//", "/")
    if url[-1:] != "/":
        return url
    return url[:-1]


def make_slug(butterfly: str) -> str:
    """Create a slug_name that's generally URL safe from any given string.
    :unit-test: TestMisc::test__make_slug
    """
    if not butterfly:
        return butterfly
    slug = butterfly.replace(" ", "-")
    slug = slug.replace("!", "")
    return slug.lower()


def find_cve(the_string: str) -> str:
    """Take a string of text and extract a CVE number is one is present, otherwise return False.
    :unit-test: TestMisc::test__find_cve
    """
    pattern = r"CVE-\d{4}-\d{1,6}"
    match = re.search(pattern, the_string)
    if not match:
        return False
    return match.group()


def key_list_on(elements: list, key="id") -> dict:
    """"Create a dictionary keyed on a given `key`."""
    ret = {}
    for element in elements:
        ret[element.id] = element
    return ret


def import_string(module_name: str):
    """Takes a python module name such as "cli_image" and creates the path for the class as well,
    assuming it follows typical Python conventions.
    IE: "cli_image" will return "cli_image.CliImage"
    :unit-test: TestMisc::test_import_string
    """
    the_meat = module_name
    underscores = module_name.count("_")
    the_class = ""
    count = 1
    while count <= underscores:
        the_class += the_meat[:the_meat.find("_")].title()
        the_meat = the_meat[the_meat.find("_") + 1:]
        count += 1

    the_class = the_class + the_meat.title()
    ret = {
        "module": module_name,
        "class": the_class
    }
    return ret


def dynamic_import(the_module: str, the_class: str):
    """Dynamically import a Python class by it's dot notation, ie "pignus.cli.cli_image.CliImage".
    :unit-test: TestMisc::test_dynamic_import
    """
    module = importlib.import_module(the_module)
    return getattr(module, the_class)


def short_digest(original_digest: str) -> str:
    """Get the short version of a Docker container SHA digest.
    ie: 572030415db278044988e6dd41e3ea414dddd0518b43368352e6e719e2610ecc -> 572030415db2
    """
    if original_digest and len(original_digest) > 12:
        return original_digest[:12]
    return ""


def docker_url(image, image_build) -> str:
    """Create the best possible url for a container based on the information the Image and
    ImageBuild contain.
    """
    docker_url = "%(repository)s%(name)s:%(tag)s%(digest)s" % {
        "repository": image_build.repository,
        "name": image.name,
        "tag": image_build.tag,
        "digest": "@sha256:%s" % image_build.digest
    }
    return docker_url


# End File: politeauthority/pignus/src/pignus_shared/utils/misc.py
