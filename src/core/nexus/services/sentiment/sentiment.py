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