import copy
import random
import torch

from core.nexus.services.vectorizer import Tokenizer



class Vectorizer(torch.nn.Module):

	def __init__(self, corpus: list[str], **config: any):

		super().__init__()

		self.tokenizer = Tokenizer()
		self.tokenizer.fit(corpus)
		
		self.dimension = config.get("dimension", 64)
		self.sequence_length = config.get("sequence_length", 128)
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
			batch_first = True
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
			indices = indices[:self.positional.encoder.size(1)]
			indices = indices + [self.tokenizer.index_padding] * (self.positional.encoder.size(1) - len(indices))
			
			batches.append(indices)

		tensor = torch.tensor(batches, dtype = torch.long, device = self.embedding.weight.device)
		padding_mask = tensor.eq(self.tokenizer.index_padding)

		tensor = self.embedding(tensor) * self.scale
		tensor = self.positional(tensor)

		hidden = self.encoder(tensor, src_key_padding_mask = padding_mask)

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
			masked_indices = torch.full((batch_dimension, layer_dimension), self.tokenizer.index_padding, dtype = torch.long)
			masked_texts = []

			for i, text in enumerate(batch):

				indices = self.tokenizer.encode(text)
				length = min(len(indices), layer_dimension - 1)

				masked_indices[i, 1 : length + 1] = torch.tensor(indices[:length], dtype = torch.long) # [0] = <CLASS>

				for j in range(length):

					if random.random() < self.masking_rate:

						labels[i, j + 1] = indices[j]
						masked_indices[i, j + 1] = self.tokenizer.index_mask

				masked_texts.append(self.tokenizer.decode([int(index) for index in list(masked_indices[i])]))

			return masked_texts, labels

class PositionalEncoder(torch.nn.Module):

	def __init__(self, **config: any):

		super().__init__()

		self.dimension = config.get("dimension", 64)
		self.sequence_length = config.get("sequence_length", 128)
		self.dropout_rate = config.get("dropout_rate", 0.1)
		
		self.dropout = torch.nn.Dropout(p = self.dropout_rate)
		
		encoder = torch.zeros(self.sequence_length, self.dimension)
		position = torch.arange(self.sequence_length).unsqueeze(1).float()
		term = torch.exp(torch.arange(0, self.dimension, 2).float() * (-torch.log(torch.tensor(10000.0)) / self.dimension))
		encoder[:, 0::2] = torch.sin(position * term)
		encoder[:, 1::2] = torch.cos(position * term)
		encoder = encoder.unsqueeze(0)

		self.register_buffer("encoder", encoder)

	def forward(self, x):

		x = x + self.encoder[:, :x.size(1), :]
		x = self.dropout(x)

		return x
