import random
import torch

from core.nexus.vectorizer.tokenizer import Tokenizer



class Vectorizer(torch.nn.Module):

	def __init__(self, settings, **config: any):

		super().__init__()

		self.tokenizer = Tokenizer(settings)
		self.tokenizer.load()
		
		self.dimension = config.get("dimension", 32)
		self.sequence_length = config.get("sequence_length", 128)
		self.dropout_rate = config.get("dropout_rate", 0.1)
		self.masking_rate = config.get("masking_rate", 0.15)
		self.number_heads = config.get("number_heads", 2)
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

		self.decoder = torch.nn.Linear(self.dimension, self.tokenizer.size, bias = True)
		self.decoder.weight = self.embedding.weight if self.tie_weights else self.decoder.weight
		torch.nn.init.zeros_(self.decoder.bias)

	def forward(self, tensor: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:

		mask = tensor.eq(self.tokenizer.index_padding)
		
		embedding = self.embedding(tensor)
		positional = self.positional(embedding)
		hidden = self.encoder(positional, src_key_padding_mask = mask)
		output = self.decoder(hidden)

		return hidden, embedding, output

	def preprocess(self, texts: list[str], device: torch.device = torch.device("cpu")) -> torch.Tensor:

		batch_dimension = len(texts)
		layer_dimension = self.sequence_length

		input_indices = torch.full((batch_dimension, layer_dimension), self.tokenizer.index_padding, dtype = torch.long)

		for i, text in enumerate(texts):

			indices = self.tokenizer.encode(text)
			length = min(len(indices), layer_dimension - 1)

			input_indices[i, 0] = self.tokenizer.index_class
			input_indices[i, 1 : length + 1] = torch.tensor(indices[:length], dtype = torch.long)

		return input_indices.to(device)

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

			for i, text in enumerate(batch):

				indices = self.tokenizer.encode(text)
				length = min(len(indices), layer_dimension - 1)

				masked_indices[i, 0] = self.tokenizer.index_class
				masked_indices[i, 1 : length + 1] = torch.tensor(indices[:length], dtype = torch.long)

				for j in range(length):

					if random.random() < self.masking_rate:

						labels[i, j + 1] = indices[j]

						probability = random.random()

						if probability < 0.8:

							masked_indices[i, j + 1] = self.tokenizer.index_mask

						elif probability < 0.9:
							
							masked_indices[i, j + 1] = random.randrange(self.tokenizer.size)

						else:

							masked_indices[i, j + 1] = indices[j]


			return masked_indices, labels

class PositionalEncoder(torch.nn.Module):

	def __init__(self, **config: any):

		super().__init__()

		self.dimension = config.get("dimension", 32)
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

	def forward(self, x: torch.Tensor) -> torch.Tensor:

		x = x + self.encoder[:, :x.size(1), :]
		x = self.dropout(x)

		return x
