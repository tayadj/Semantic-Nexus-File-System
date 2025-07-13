import pathlib

from core.system.architecture.operations import CreateOperation



class Manager:

	def __init__(self, settings):

		self.settings = settings

	def create(self, uri: str, data: str):

		uri = pathlib.Path(f"{self.settings.system.root}/{uri}.meta")
		data = data.encode()

		operation = CreateOperation(uri, data) # instead of str/byte array -> node object to save

		try:

			operation.execute()

		except Exception as exception:

			print(f"Oops! {exception}")
			operation.rollback()

# implement dynamic operations declaration as is engine from nexus, each operation in its own file