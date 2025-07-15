import pathlib



class Read:

	def __init__(self, uri: pathlib.Path):

		self.uri = uri

	def execute(self) -> bytes:

		return self.uri.read_bytes()
		
	def rollback(self):

		pass