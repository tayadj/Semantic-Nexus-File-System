import torch

from core.nexus.services import Vectorizer, Sentifier, Entifier



class Engine:

	def __init__(self):

		self.vectorizer = None
		self.sentifier = None
		self.entifier = None

		self.device = torch.device("cpu")