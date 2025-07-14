import pathlib



class Write:

	def __init__(self, uri: pathlib.Path, data: bytes):

		self.uri = uri
		self.data = data
		self.existed = uri.exists()
		self.backup = uri.read_bytes() if self.existed else None

	def execute(self) -> bytes:

		self.uri.parent.mkdir(parents = True, exist_ok = True)
		self.uri.write_bytes(self.data)

		return self.data

	def rollback(self):

		if self.existed:

			self.uri.write_bytes(self.backup)

		else:

			if self.uri.exists():

				self.uri.unlink()

