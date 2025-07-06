import torch

from core.nexus.services.vectorizer import Tokenizer



class Vectorizer(torch.nn.Module):

	def __init__(self, dimension):

		super().__init__()

		self.tokenizer = Tokenizer()
		self.embedding = None

		self.dimension = dimension

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