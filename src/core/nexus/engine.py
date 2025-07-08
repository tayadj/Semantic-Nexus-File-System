import copy
import torch

from core.nexus.services import Vectorizer, Sentifier, Entifier



class Engine:

	def __init__(self):

		self.vectorizer = Vectorizer(dimension = 128)
		self.sentifier = None
		self.entifier = None

		self.device = torch.device("cpu")
		
	def build(self, corpus):

		self.vectorizer.fit(corpus)

		self.sentifier = Sentifier(copy.deepcopy(self.vectorizer))
		self.entifier = Entifier(copy.deepcopy(self.vectorizer))