import torch



class Sentifier(torch.nn.Module):

	def __init__(self, vectorizer):

		super().__init__()

		self.vectorizer = vectorizer
		self.hidden = torch.nn.Linear(vectorizer.dimension, 128)
		self.output = torch.nn.Linear(128, 2)

	def forward(self, texts):

		x = self.vectorizer(texts)
		x = x.mean(dim = 1)
		x = self.hidden(x)
		x = torch.relu(x)
		x = self.output(x)
		
		return x

	class Dataset(torch.utils.data.Dataset):

		def __init__(self, texts, labels):

			self.texts = texts
			self.labels = labels

		def __len__(self):

			return len(self.texts)

		def __getitem__(self, index):

			text = self.texts[index]
			label = torch.tensor(self.labels[index], dtype = torch.long)

			return text, label

		def collate(self, batch):

			texts, labels = zip(*batch)

			return list(texts), torch.stack(labels)