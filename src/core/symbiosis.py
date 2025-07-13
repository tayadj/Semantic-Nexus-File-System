from core.nexus import Engine
from core.system import Manager



# implement agentic approach with tools as functions (or MCP) for CRUD-etc.

class Symbiosis:

	def __init__(self, settings):

		self.engine = Engine(settings)
		self.manager = Manager(settings)

	def create(self, uri: str, data: str) -> None:

		metadata = {}

		for service, instance in self.engine.services.items():

			metadata[service] = instance.inference([data]) if service != "vectorizer" else ...

		return self.manager.create(uri, data, metadata)