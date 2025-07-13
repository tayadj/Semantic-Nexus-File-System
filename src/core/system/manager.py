import pathlib

from core.system.architecture.objects import Node
from core.system.architecture.operations import CreateOperation




class Manager:

	def __init__(self, settings):

		self.settings = settings

	def create(self, uri: str, data: str, metadata: dict):

		uri = pathlib.Path(f"{self.settings.system.root}/{uri}.meta")
		data = data.encode()
		node = Node(uri, data, metadata)
		serialized = node.serialize()

		operation = CreateOperation(uri, serialized)

		try:

			operation.execute()

		except Exception as exception:

			print(f"Oops! {exception}")
			operation.rollback()

# implement dynamic operations declaration as is engine from nexus, each operation in its own file