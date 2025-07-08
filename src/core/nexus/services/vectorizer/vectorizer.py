import copy
import torch

from core.nexus.services.vectorizer import Tokenizer



class Vectorizer(torch.nn.Module):

	def __init__(self, dimension):

		super().__init__()

		self.dimension = dimension

		self.tokenizer = Tokenizer()
		self.embedding = None

	def __deepcopy__(self, memo):

		instance = self.__class__(self.dimension)

		memo[id(self)] = instance

		instance.dimension = self.dimension
		instance.tokenizer = self.tokenizer

		instance.embedding = torch.nn.Embedding(
			num_embeddings = self.embedding.num_embeddings,
			embedding_dim = self.embedding.embedding_dim,
			padding_idx = self.embedding.padding_idx
		)

		state = copy.deepcopy(self.embedding.state_dict(), memo)
		instance.embedding.load_state_dict(state)

		return instance

	def fit(self, corpus):

		self.tokenizer.fit(corpus)
		self.embedding = torch.nn.Embedding(
			num_embeddings = self.tokenizer.size,
			embedding_dim = self.dimension,
			padding_idx = self.tokenizer.index_padding
		)

	def forward(self, texts):

		batches = [ torch.LongTensor(self.tokenizer.encode(text)) for text in texts ]
		padded = torch.nn.utils.rnn.pad_sequence(batches, batch_first = True, padding_value = self.tokenizer.index_padding)
		embedding = self.embedding(padded)

		return embedding.mean(dim = 1)