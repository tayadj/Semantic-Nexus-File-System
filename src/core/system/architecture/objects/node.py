import pathlib
import pickle



class Node:

	def __init__(self, uri: pathlib.Path = None, data: bytes = None, metadata: dict = None):

		self.uri = uri
		self.data = data
		self.metadata = metadata

	def __str__(self) -> str:
		
		return f"<Node {self.uri.name}: size = {len(self.serialize())} bytes, data = {self.data}, metadata = {self.metadata}>"

	def serialize(self) -> bytes:

		return pickle.dumps(self)

	def deserialize(self, blob: bytes) -> None:

		object = pickle.loads(blob)
		self.uri = object.uri
		self.data = object.data
		self.metadata = object.metadata
