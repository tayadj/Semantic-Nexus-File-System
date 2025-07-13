import pathlib



class Operation:

	def execute(self) -> None:

		...

	def rollback(self) -> None:

		...



class CreateOperation(Operation):

	def __init__(self, uri: pathlib.Path, data: bytes):

		self.uri = uri
		self.data = data

	def execute(self):

		self.uri.parent.mkdir(parents = True, exist_ok = True)
		self.uri.write_bytes(self.data)

	def rollback(self):

		if self.uri.exists():

			self.uri.unlink()