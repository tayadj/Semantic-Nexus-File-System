import torch



class Sentifier(torch.nn.Module):

	def __init__(self, **config: any):

		super().__init__()

		self.embedding = config.get("embedding", 64)
		self.dimension = config.get("dimension", 128)
		self.number_classes = config.get("number_classes", 2)

		self.hidden = torch.nn.Linear(self.embedding, self.dimension)
		self.inter = torch.nn.Linear(self.dimension, self.dimension)
		self.output = torch.nn.Linear(self.dimension, self.number_classes)

	def forward(self, embedding):

		x = self.hidden(embedding)
		x = torch.relu(x)
		x = self.inter(x)
		x = torch.relu(x)
		x = self.output(x)
		
		return x

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
			
				hidden, _ = self.vectorizer(list(texts))
			
			embeddings = hidden[:, 0, :].detach()

			labels = torch.stack(labels)

			return embeddings, labels