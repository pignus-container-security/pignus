"""Pignus-Sentry: Primary EntryPoint
Pignus-Sentry runs all the backend operations of container syncing and scanning.

"""
from pignus_client import PignusClient
from pignus_shared.utils import log


class PignusSentry:

    def __init__(self):
        self.pigus_api = PignusClient()

    def run(self):
        print("Running Pignus Sentry")
        self.sentry_scan()

    def sentry_scan(self):
        """Collect ImageBuilds requiring a scan and run them through the given scanner."""
        log.info("Sentry Scan")
        image_builds = self.get_scan_image_builds()
        for image_build in image_builds:
            log.info("%s\t-%s" % (image_build["id"], image_build["image_id"]))
            self.scan_build(image_build)

    def get_scan_image_builds(self) -> list:
        """Get ImageBuilds ready for scan."""
        request = self.pigus_api.image_builds_get_for_scan()
        requset_data = request.json()
        import ipdb; ipdb.set_trace()
        log.info("Found %s ImageBuilds for scan" % requset_data["object_count"])
        log.info("ImagesBuilds")
        return requset_data["objects"]

    def scan_build(self, image_build_raw):
        """Scan a single build from the ImageBuild presented."""
        image_id = image_build_raw["image_id"]
        image_build = ImageBuild()
        image_build.build_from_dict(image_build_raw)
        image = self.pigus_api.object_get_by_id("image", image_id)
        print(image)
        # import ipdb; ipdb.set_trace()


if __name__ == "__main__":
    PignusSentry().run()


# End File: pignus/src/pignus_sentry/pignus_sentry.py
