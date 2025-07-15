import torch

from core.system.architecture.operations import operations



class Router(torch.nn.Module):

	def __init__(self, **config: any):

		super().__init__()

		self.embedding = config.get("embedding", 32)
		self.dimension = config.get("dimension", 128)
		self.number_layers = config.get("number_layers", 2)
		self.dropout = config.get("dropout", 0.1)

		self.operation_to_index = {
			operation : index
			for index, operation in enumerate(operations.keys())
		}
		self.index_to_operation = { index : operation for operation, index in self.operation_to_index.items() }
		self.operation_undefined = len(self.operation_to_index)
		self.operation_size = len(self.operation_to_index) + 1

		self.hidden = torch.nn.LSTM(
			input_size = self.embedding,
			hidden_size = self.dimension,
			num_layers = self.number_layers,
			dropout = self.dropout if self.number_layers > 1 else 0.0,
			bidirectional = True,
			batch_first = True
		)
		self.classifier = torch.nn.Linear(self.dimension * 2, self.operation_size)

	def forward(self, embeddings: torch.Tensor) -> torch.Tensor:

		_, (hidden, _) = self.hidden(embeddings)

		hidden_forward = hidden[-2]
		hidden_backward = hidden[-1]
		hidden = torch.cat([hidden_forward, hidden_backward], dim = 1)

		logits = self.classifier(hidden)

		return logits

	class Dataset(torch.utils.data.Dataset):

		def __init__(self, texts: list[str], labels: list[str], vectorizer, operation_to_index):

			self.texts = texts
			self.labels = labels

			self.vectorizer = vectorizer

			self.operation_to_index = operation_to_index
			self.index_to_operation = { index : operation for operation, index in self.operation_to_index.items() }
			self.operation_undefined = len(self.operation_to_index)
			self.operation_size = len(self.operation_to_index) + 1

		def __len__(self):

			return len(self.texts)

		def __getitem__(self, index):

			text = self.texts[index]
			label = self.labels[index]

			return text, label

		def collate(self, batch):

			texts, labels = zip(*batch)

			with torch.no_grad():
			
				_, embeddings, _ = self.vectorizer(self.vectorizer.preprocess(texts))
			
			labels = torch.tensor([self.operation_to_index.get(label, self.operation_undefined) for label in labels], dtype = torch.long)

			return embeddings, labels
