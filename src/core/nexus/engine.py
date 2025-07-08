import copy
import torch

from core.nexus.services import Vectorizer, Sentiment



class Engine:

	def __init__(self):

		self.vectorizer = Vectorizer(dimension = 128)
		self.sentiment = None

		self.device = torch.device("cpu")
		
	def build(self, corpus):

		self.vectorizer.fit(corpus)

		self.sentiment = Sentiment(copy.deepcopy(self.vectorizer))