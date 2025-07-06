import torch



class Sentiment(torch.nn.Module):

	def __init__(self, vectorizer):

		super().__init__()

		self.vectorizer = vectorizer
		self.hidden = torch.nn.Linear(vectorizer.dimension, 32)
		self.output = torch.nn.Linear(32, 2)

	def forward(self, texts):

		x = self.vectorizer(texts)
		x = self.hidden(x)
		x = torch.relu(x)
		x = self.output(x)
		
		return x

class Dataset(torch.utils.data.Dataset):

	def __init__(self, texts, labels, tokenizer):

		self.texts = texts
		self.labels = labels
		self.tokenizer = tokenizer

	def __len__(self):

		return len(self.texts)

	def __getitem__(self, index):

		indices = torch.LongTensor(self.tokenizer.encode(self.texts[index]))
		label = torch.tensor(self.labels[index], dtype = torch.long)

		return indices, label

def collate(batch):

	texts, labels = zip(*batch)
	padded = torch.nn.utils.rnn.pad_sequence(texts, batch_first = True, padding_value = 0)

	return padded, torch.stack(labels)