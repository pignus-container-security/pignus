"""Pignus-Shared: Util - Docker
Utilities for working with the Docker engine locally.

"""
import subprocess

from pignus_shared.utils import log
from pignus_shared.utils import misc


def run_trivy_scan(image_str: str):
    trivy_image = "aquasec/trivy:0.18.3"
    cmd = "docker run --rm %s %s" % (trivy_image, image_str)
    print(cmd)


def get_host_docker_images() -> list:
    """Get Docker images on the host machine."""
    cmd = "docker ps --format '{{ .ID }},{{.Image}}' --no-trunc"
    try:
        docker_ps = subprocess.check_output(cmd, shell=True)
    except subprocess.CalledProcessError as e:
        log.error("Error fetching data from Docker: %s" % e)
        return False
    images = _parse_docker_ps(docker_ps)
    return images


def _parse_docker_ps(docker_ps: str) -> list:
    """Parse the output from the docker ps command."""
    docker_ps = docker_ps.decode()
    lines = docker_ps.split("\n")
    images = []
    for line in lines:
        if not line:
            continue
        split = line.split(",")
        digest = split[0]
        url = split[1]
        image = misc.parse_image_url(url)
        image["digest"] = digest
        images.append(image)
    return images

# End File: pignus/src/pignus_shared/utils/docker.py
