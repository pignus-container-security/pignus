"""Submit Docker Containers

"""
import subprocess

from pignus_client import PignusClient
from pignus_shared.utils import misc
from pignus_shared.utils import log
from pignus_shared.utils import docker


class PignusDockerImages:

	def __init__(self):
		self.pignus = PignusClient()

	def run(self):
		print("Running")
		images = docker.get_host_docker_images()
		if not images:
			exit(1)

		print("Found %s Images to submit to Pignus" % len(images))
		for image in images:
			self.add_image(image)

		print("DONE")

	def add_image(self, image_url):
		log.info("Submitting: %s" % image_url["full"])
		response = self.pignus.image_add(image_url)
		if response.status_code >= 200:
			log.info("%s - Success" % response.status_code)
		else:
			log.error("%s - Error\t%s" % response.status_code, response.text)



if __name__ == "__main__":
	PignusDockerImages().run()
