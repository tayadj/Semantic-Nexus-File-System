import torch

from core.nexus.services import Sentifier, Entifier
from core.nexus.services.vectorizer import Processor as Vectorizer



class Engine:

	def __init__(self):

		self.vectorizer = None
		self.sentifier = None
		# self.entifier = None

		self.device = torch.device("cpu")

	def setup(self, settings):

		self.vectorizer = Vectorizer(settings)
		self.sentifier = torch.load(settings.sentifier.path, weights_only = False)

	# Pipelines for services, pipelines' configuration must be within model structure