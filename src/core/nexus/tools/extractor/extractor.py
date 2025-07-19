import torch



# Outdated

class Extractor(torch.nn.Module):

	def __init__(self, **config: any):

		super().__init__()

		self.embedding = config.get("embedding", 32)
		self.dimension = config.get("dimension", 128)
		self.number_layers = config.get("number_layers", 2)
		self.dropout = config.get("dropout", 0.1)

		self.NER_to_index = { "O": 0, "B-INPUT": 1, "I-INPUT": 2 }
		self.index_to_NER = { index : tag for tag, index in self.NER_to_index.items() }
		self.NER_padding_index = len(self.NER_to_index)
		self.NER_size = len(self.NER_to_index) + 1

		self.hidden = torch.nn.LSTM(
			input_size = self.embedding,
			hidden_size = self.dimension,
			num_layers = self.number_layers,
			dropout = self.dropout if self.number_layers > 1 else 0.0,
			bidirectional = True,
			batch_first = True
		)
		self.classifier = torch.nn.Linear(self.dimension * 2, self.NER_size)

	def forward(self, embeddings: torch.Tensor) -> torch.Tensor:

		hidden, _ = self.hidden(embeddings)
		logits = self.classifier(hidden)

		return logits

	class Dataset(torch.utils.data.Dataset):

		def __init__(self, texts: list[str], labels: list[str], vectorizer, NER_to_index):

			self.texts = texts
			self.labels = labels

			self.vectorizer = vectorizer

			self.NER_to_index = NER_to_index
			self.index_to_NER = { index : tag for tag, index in NER_to_index.items() }
			self.NER_padding_index = len(NER_to_index)
			self.NER_size = len(NER_to_index) + 1

		def map_NER(self, input):

			return [self.NER_to_index.get(tag, self.NER_padding_index) for tag in input]

		def __len__(self):

			return len(self.texts)

		def __getitem__(self, index):

			text = self.texts[index]
			label = self.labels[index]

			return text, label

		def collate(self, batch):

			texts, raw_labels = zip(*batch)

			with torch.no_grad():
			
				_, embeddings, _ = self.vectorizer(self.vectorizer.preprocess(texts))

			batch_dimension, layer_dimension, _ = embeddings.shape		
			labels = torch.full((batch_dimension, layer_dimension), self.NER_padding_index, dtype = torch.long)

			for i, raw_label in enumerate(raw_labels):

				indices = self.map_NER(raw_label)
				length = min(len(indices), layer_dimension - 1)
				labels[i, 1 : length + 1] = torch.tensor(indices[:length], dtype = torch.long)

			return embeddings, labels
