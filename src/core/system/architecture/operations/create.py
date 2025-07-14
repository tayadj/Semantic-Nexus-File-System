import pathlib



class Create:

	def __init__(self, uri: pathlib.Path):

		self.uri = uri
		self.existed = uri.exists()

	def execute(self) -> None:

		self.uri.parent.mkdir(parents = True, exist_ok = True)
		self.uri.touch(exist_ok = True)

	def rollback(self):

		if self.uri.exists() and not self.existed:

			self.uri.unlink()

