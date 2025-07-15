from core.nexus import Engine
from core.system import Manager



class Symbiosis:

	# class Agent

	def __init__(self, settings):

		self.engine = Engine(settings)
		self.manager = Manager(settings)

	def metafy(self, data: str) -> tuple[str, dict]:

		metadata = {}

		for service, instance in self.engine.services.items():

			metadata[service] = instance.inference([data])[0] if service != "vectorizer" else ...

		return (data, metadata)

	def query(self, query: str):

		operation = self.engine.tools["router"].inference([query])[0]
		arguments = self.engine.tools["extractor"].inference([query])[0]
		operation = getattr(self.manager, operation, None)

		if len(arguments) > 1:

			data, metadata = self.metafy(arguments[1])
			arguments = [arguments[0], data, metadata]

		if operation and arguments:

			return operation(*arguments)