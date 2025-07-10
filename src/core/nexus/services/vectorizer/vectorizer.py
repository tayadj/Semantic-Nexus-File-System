import copy
import random
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

		return embedding



class PositionalEncoder(torch.nn.Module):

	def __init__(self, **config: any):

		super().__init__()

		self.dimension = config.get("dimension", 64)
		self.sequence_length = config.get("sequence_length", 512)
		self.dropout_rate = config.get("dropout_rate", 0.1)
		
		self.dropout = torch.nn.Dropout(p = self.dropout_rate)
		
		encoder = torch.zeros(self.sequence_length, self.dimension)
		position = torch.arange(0, self.sequence_length, dtype = torch.float).unsqueeze(1)
		term = torch.exp(torch.arange(0, self.dimension, 2).float() * float(-torch.log(torch.Tensor([10000.0])) / self.dimension))
		encoder[:, 0::2] = torch.sin(position * term)
		encoder[:, 1::2] = torch.cos(position * term)
		encoder = encoder.unsqueeze(0).transpose(0, 1)

		self.register_buffer("encoder", encoder)

	def forward(self, x):

		x = x + self.encoder[:x.size(0), :]
		x = self.dropout(x)

		return x

class TransformerVectorizer(torch.nn.Module):

	def __init__(self, corpus: list[str], **config: any):

		super().__init__()

		self.tokenizer = Tokenizer()
		self.tokenizer.fit(corpus)
		
		self.dimension = config.get("dimension", 64)
		self.sequence_length = config.get("sequence_length", 512)
		self.dropout_rate = config.get("dropout_rate", 0.1)
		self.masking_rate = config.get("masking_rate", 0.15)
		self.number_heads = config.get("number_heads", 4)
		self.number_layers = config.get("number_layers", 2)
		self.feedforward = config.get("feedforward", 128)
		self.tie_weights = config.get("tie_weights", True)

		self.embedding = torch.nn.Embedding(self.tokenizer.size, self.dimension, padding_idx = self.tokenizer.index_padding)
		self.positional = PositionalEncoder(dimension = self.dimension, sequence_length = self.sequence_length, dropout_rate = self.dropout_rate)

		self.encoder_layer = torch.nn.TransformerEncoderLayer(
			d_model = self.dimension,
			nhead = self.number_heads,
			dim_feedforward = self.feedforward,
			dropout = self.dropout_rate,
			batch_first = True # True? False doesn't involves nested tensors
		)
		self.encoder = torch.nn.TransformerEncoder(
			self.encoder_layer,
			self.number_layers
		)

		self.decoder = torch.nn.Linear(self.dimension, self.tokenizer.size, bias = False)
		self.decoder.weight = self.embedding.weight if self.tie_weights else self.decoder.weight

		self.scale = self.dimension ** 0.5

	def forward(self, texts: list[str]) -> tuple[torch.Tensor, torch.Tensor]:

		batches = []

		for text in texts:

			indices = self.tokenizer.encode(text)
			indices = [self.tokenizer.index_class] + indices
			indices = indices[:self.positional.encoder.size(0)]
			indices = indices + [self.tokenizer.index_padding] * (self.positional.encoder.size(0) - len(indices))
			
			batches.append(indices)

		tensor = torch.tensor(batches, dtype = torch.long)

		tensor = self.embedding(tensor) * self.scale
		tensor = self.positional(tensor)

		hidden = self.encoder(tensor)

		output = self.decoder(hidden)

		return hidden, output

	class Dataset(torch.utils.data.Dataset):

		def __init__(self, corpus: list[str], tokenizer, sequence_length, masking_rate):

			self.corpus = corpus
			self.tokenizer = tokenizer
			self.sequence_length = sequence_length
			self.masking_rate = masking_rate

		def __len__(self):

			return len(self.corpus)

		def __getitem__(self, index):

			return self.corpus[index]

		def collate(self, batch: list[str]):

			batch_dimension = len(batch)
			layer_dimension = self.sequence_length

			labels = torch.full((batch_dimension, layer_dimension), -1, dtype = torch.long)
			masked = []

			for i, text in enumerate(batch):

				indices = self.tokenizer.encode(text)
				length = len(indices)
				indices_ = [self.tokenizer.index_class] + indices
				indices_ = indices_[:layer_dimension]
				indices_ = indices_ + [self.tokenizer.index_padding] * (layer_dimension - len(indices_))
				labels[i] = torch.tensor(indices_, dtype = torch.long)

				mask = [False] * length

				for j in range(length):

					if random.random() < self.masking_rate:

						mask[j] = True

				masked_indices = []

				for j, index in enumerate(indices):

					masked_indices.append(self.tokenizer.index_mask if mask[j] else index)

				masked_text = self.tokenizer.decode(masked_indices)
				masked.append(masked_text)

			return masked, labels
