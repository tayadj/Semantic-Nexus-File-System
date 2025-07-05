from .services import Vectorizer


class Engine:

	def __init__(self):

		self.vectorizer = Vectorizer(dimension = 128)