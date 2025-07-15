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