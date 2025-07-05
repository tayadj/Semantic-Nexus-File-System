from .embedding import Embedding
from .tokenizer import Tokenizer


class Vectorizer:

	def __init__(self):

		self.tokenizer = Tokenizer()
		self.embedding = Embedding()