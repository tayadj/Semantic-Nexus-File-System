from core.nexus.services import Vectorizer, Sentiment


class Engine:

	def __init__(self):

		self.vectorizer = Vectorizer(dimension = 128)
		self.sentiment = Sentiment(self.vectorizer)