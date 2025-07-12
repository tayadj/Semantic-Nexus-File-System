import torch


class Sentifier(torch.nn.Module):

	def __init__(self, **config: any):

		super().__init__()

		self.embedding = config.get("embedding", 32)
		self.dimension = config.get("dimension", 128)
		self.number_classes = config.get("number_classes", 2)
		self.number_layers = config.get("number_layers", 2)
		self.dropout = config.get("dropout", 0.1)

		self.hidden = torch.nn.LSTM(
			input_size = self.embedding,
			hidden_size = self.dimension,
			num_layers = self.number_layers,
			dropout = self.dropout if self.number_layers > 1 else 0.0,
			bidirectional = True,
			batch_first = True
		)
		self.classifier = torch.nn.Linear(self.dimension * 2, self.number_classes)

	def forward(self, embeddings: torch.Tensor) -> torch.Tensor:

		_, (hidden, _) = self.hidden(embeddings)

		hidden_forward = hidden[-2]
		hidden_backward = hidden[-1]
		hidden = torch.cat([hidden_forward, hidden_backward], dim = 1)

		logits = self.classifier(hidden)

		return logits

	class Dataset(torch.utils.data.Dataset):

		def __init__(self, texts, labels, vectorizer):

			self.texts = texts
			self.labels = labels
			self.vectorizer = vectorizer

		def __len__(self):

			return len(self.texts)

		def __getitem__(self, index):

			text = self.texts[index]
			label = torch.tensor(self.labels[index], dtype = torch.long)

			return text, label

		def collate(self, batch):

			texts, labels = zip(*batch)

			with torch.no_grad():
			
				_, static_embedding, _ = self.vectorizer(self.vectorizer.preprocess(texts))
			
			embeddings = static_embedding
			labels = torch.stack(labels)

			return embeddings, labels
