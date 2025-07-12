import torch

from core.nexus.services import Vectorizer, Sentifier, Entifier



class Engine:

	def __init__(self):

		self.vectorizer = None
		self.sentifier = None
		# self.entifier = None

		self.device = torch.device("cpu")

	def setup(self, settings):

		self.vectorizer = torch.load(settings.vectorizer.path, weights_only = False)
		self.sentifier = torch.load(settings.sentifier.path, weights_only = False)

	# Pipelines for services, pipelines' configuration must be within model structure