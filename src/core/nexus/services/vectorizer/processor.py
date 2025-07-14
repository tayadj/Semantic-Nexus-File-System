import pandas
import torch

from core.nexus.services.vectorizer.vectorizer import Vectorizer
from core.nexus.services.vectorizer.tokenizer import Tokenizer



class Processor:

	def __init__(self, settings):

		self.settings = settings
		self.device = torch.device(self.settings.device)
		self.model = None

	def load(self):

		self.model = torch.load(self.settings.vectorizer.model, weights_only = False)
		self.model.to(self.device)

	def save(self):

		torch.save(self.model, self.settings.vectorizer.model)

	def data(self) -> list[str]:

		data = pandas.read_json(self.settings.vectorizer.data, orient = "records")

		return data["text"].tolist()

	def train(self, data: list[str], **config: any):

		self.model.train()

		epochs = config.get("epochs", 10)
		iterations = config.get("iterations", 1000)
		batch_size = config.get("batch_size", 8)
		learning_rate = config.get("learning_rate", 1e-4)

		dataset = self.model.Dataset(data, self.model.tokenizer, self.model.sequence_length, self.model.masking_rate)
		loader = torch.utils.data.DataLoader(dataset, batch_size = batch_size, shuffle = True, collate_fn = dataset.collate)

		optimizer = torch.optim.AdamW(self.model.parameters(), lr = learning_rate)
		criterion = torch.nn.CrossEntropyLoss(ignore_index = -1)

		for epoch in range(1, epochs + 1):

			total_loss = 0.0
			iteration_counter = 0

			for indices, labels in loader:

				if iteration_counter > iterations:

					break

				indices = indices.to(self.device)
				labels = labels.to(self.device)

				optimizer.zero_grad()
				_, _, output = self.model(indices)
				logits = output.view(-1,  output.size(-1))
				targets = labels.view(-1)
				loss = criterion(logits, targets)
				loss.backward()
				optimizer.step()

				total_loss += loss.item()
				iteration_counter += 1

			average_loss = total_loss / iteration_counter
			print(f"Epoch {epoch}/{epochs}, Loss: {average_loss:.4f}")

	def inference(self, data: list[str]):

		self.model.eval()

		with torch.no_grad():

			data = self.model.preprocess(data)
			_, embeddings, _ = self.model(data)

		return embeddings

