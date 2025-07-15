import torch

from core.nexus.services import services
from core.nexus.agent import tools



class Engine:

	def __init__(self, settings):

		self.settings = settings
		self.services = { service : instance(self.settings) for service, instance in services.items() }
		self.tools = { tool: instance(self.settings) for tool, instance in tools.items()}

		self.build()

	def build(self):

		for service in self.services.values():

			try:

				service.load()

			except:

				...