import torch

from core.nexus.services import services



class Engine:

	def __init__(self, settings):

		self.settings = settings
		self.services = { service : instance(self.settings) for service, instance in services.items() }
		self.build()

	def build(self):

		for service in self.services.values():

			try:

				service.load()

			except:

				...