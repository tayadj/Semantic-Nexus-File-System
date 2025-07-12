import torch


class Entifier(torch.nn.Module):

	pass


'''
class OutdatedEntifier(torch.nn.Module):

	def __init__(self, vectorizer):

		super().__init__()

		self.vectorizer = vectorizer
		self.hidden = torch.nn.LSTM(
			input_size = vectorizer.dimension,
			hidden_size = 128,
			num_layers = 1,
			batch_first = True,
			bidirectional = True
		)
		self.output = torch.nn.Linear(128 * 2, 18) # NER_size

	def forward(self, texts):

		x = self.vectorizer(texts)
		x, _ = self.hidden(x)
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
			label = self.labels[index]

			return text, label

		def collate(self, batch):

			texts, labels = zip(*batch)

			labels = [torch.LongTensor(label) for label in labels]
			labels = torch.nn.utils.rnn.pad_sequence(labels, batch_first = True, padding_value = 17) # NER_padding_value

			return list(texts), labels
'''