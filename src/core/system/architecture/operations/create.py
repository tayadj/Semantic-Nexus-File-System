import pathlib



class Create:

	def __init__(self, uri: pathlib.Path, data: bytes):

		self.uri = uri
		self.data = data

	def execute(self) -> bytes:

		self.uri.parent.mkdir(parents = True, exist_ok = True)
		self.uri.write_bytes(self.data)

		return self.data

	def rollback(self):

		if self.uri.exists():

			self.uri.unlink()

