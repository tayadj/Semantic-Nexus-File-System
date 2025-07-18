import torch

from core.nexus.vectorizer import vectorizers
from core.nexus.services import services
from core.nexus.agent import tools



class Engine:

	def __init__(self, settings):

		self.settings = settings

		self.vectorizer = self.register(vectorizers)["vectorizer"]
		self.services = self.register(services)
		self.tools = self.register(tools)

	def register(self, components: dict[str, type]):

		instances = { component : instance(self.settings) for component, instance in components.items() }

		for instance in instances.values():

			try:

				instance.load()

			except Exception as exception:

				instance.instance()

		return instances
