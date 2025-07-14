import pandas
import torch

from core.nexus.services.sentifier.sentifier import Sentifier



class Processor:

	def __init__(self, settings):

		self.settings = settings
		self.device = torch.device(self.settings.device)
		self.model = None
		self.vectorizer = torch.load(self.settings.vectorizer.model, weights_only = False)
		self.vectorizer.to(self.device)
		self.vectorizer.eval()

	def load(self):

		self.model = torch.load(self.settings.sentifier.model, weights_only = False)
		self.model.to(self.device)

	def save(self):

		torch.save(self.model, self.settings.sentifier.model)

	def instance(self, **config: any):

		self.model = Sentifier(**config)

	def data(self) -> tuple[list[str], list[int]]:

		data = pandas.read_json(self.settings.sentifier.data, orient = "records")

		return (data["text"].tolist(), data["sentiment"].tolist())

	def train(self, data: tuple[list[str], list[int]], **config: any):

		self.model.train()

		epochs = config.get("epochs", 10)
		iterations = config.get("iterations", 1000)
		batch_size = config.get("batch_size", 2)
		learning_rate = config.get("learning_rate", 1e-3)

		dataset = self.model.Dataset(data[0], data[1], self.vectorizer)
		loader = torch.utils.data.DataLoader(dataset, batch_size = batch_size, shuffle = True, collate_fn = dataset.collate)

		optimizer = torch.optim.Adam(self.model.parameters(), lr = learning_rate)
		criterion = torch.nn.CrossEntropyLoss()

		for epoch in range(1, epochs + 1):

			total_loss = 0.0
			iteration_counter = 0

			for embeddings, labels in loader:

				if iteration_counter > iterations:

					break

				embeddings = embeddings.to(self.device)
				labels = labels.to(self.device)

				optimizer.zero_grad()
				output = self.model(embeddings)
				logits = output
				targets = labels
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

			data = self.vectorizer.preprocess(data)
			_, embeddings, _ = self.vectorizer(data)
			logits = self.model(embeddings)
			probabilities = torch.nn.functional.softmax(logits, dim = 1)
			predictions = torch.argmax(probabilities, dim = 1)

		result = ["Positive" if int(prediction) == 1 else "Negative" for prediction in predictions]

		return result
