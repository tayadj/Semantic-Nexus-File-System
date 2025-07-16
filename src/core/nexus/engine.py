import torch

from core.nexus.vectorizer import Processor
from core.nexus.services import services
from core.nexus.agent import tools



class Engine:

	def __init__(self, settings):

		self.settings = settings
		self.vectorizer = Processor(self.settings)
		self.services = { service : instance(self.settings) for service, instance in services.items() }
		self.tools = { tool: instance(self.settings) for tool, instance in tools.items()}

		self.build()

	def build(self):

		# to be refactored as a registry

		for service in self.services.values():

			try:

				service.load()

			except:

				service.instance()

		for tool in self.tools.values():

			try:

				tool.load()

			except:

				tool.instance()