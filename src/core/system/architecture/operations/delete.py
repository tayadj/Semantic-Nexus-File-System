import pathlib



class Delete:

	def __init__(self, uri: pathlib.Path):

		self.uri = uri

		self.existed = uri.exists()
		self.backup = uri.read_bytes() if self.existed else None

	def execute(self) -> None:

		if self.existed:
		
			self.uri.unlink()

	def rollback(self):

		if self.existed:

			self.uri.parent.mkdir(parents = True, exist_ok = True)
			self.uri.write_bytes(self.backup)
