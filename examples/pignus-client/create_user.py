from pignus_client import PignusClient

def run():
	pignus = PignusClient()
	print("Running")
	response = pignus.images_get()
	print(response.json())
	# print(images)
	print("DONE")


if __name__ == "__main__":
	run()
