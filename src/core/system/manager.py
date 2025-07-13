import pathlib

from core.system.architecture.objects import Node
from core.system.architecture.operations import Create, Read




class Manager:

	def __init__(self, settings):

		self.settings = settings

	def create(self, uri: str, data: str, metadata: dict) -> Node:

		uri = pathlib.Path(f"{self.settings.system.root}/{uri}.meta")
		data = data.encode()
		node = Node(uri, data, metadata)
		serialized = node.serialize()

		operation = Create(uri, serialized)

		try:

			operation.execute()

		except Exception as exception:

			print(f"Oops! {exception}")
			operation.rollback()

		return node

	def read(self, uri: str) -> Node:

		uri = pathlib.Path(f"{self.settings.system.root}/{uri}.meta")

		operation = Read(uri)

		try:

			serialized = operation.execute()
			node = Node(...)
			node.deserialize(serialized)

		except Exception as exception:

			print(f"Oops! {exception}")
			operation.rollback()

		return node

# implement dynamic operations declaration as is engine from nexus, each operation in its own file