import json
import torch

from core.nexus.services.sentifier.sentifier import Sentifier
from core.nexus.mediators.textual import Processor as Vectorizer



class Processor:

	def __init__(self, settings):

		self.settings = settings
		self.device = torch.device(self.settings.device)
		self.model = None

		self.vectorizer = Vectorizer(settings)
		self.vectorizer.load()

	def save(self):

		torch.save(self.model.state_dict(), self.settings.sentifier.model)

	def load(self):

		state = torch.load(self.settings.sentifier.model, map_location = self.device)
		
		self.instance()
		self.model.load_state_dict(state)
		self.model.to(self.device)

	def instance(self, **config: any):

		self.model = Sentifier(**config)
		self.model.to(self.device)

	def data(self) -> tuple[list[str], list[int]]:

		with open(self.settings.sentifier.data, "r", encoding = "utf-8") as file:

			data = json.load(file)

		texts, labels = zip(*data)

		return list(texts), list(labels)

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

				if iteration_counter == iterations:

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

	def inference(self, texts: list[str]):

		self.model.eval()

		with torch.no_grad():

			_, _, _, embeddings = self.vectorizer.inference(texts)
			logits = self.model(embeddings)
			probabilities = torch.nn.functional.softmax(logits, dim = 1)
			predictions = torch.argmax(probabilities, dim = 1)

		result = ["Positive" if int(prediction) == 1 else "Negative" for prediction in predictions]
		result = ["Neutral" if float(torch.max(probability)) < 0.6 else decision for decision, probability in zip(result, probabilities)]

		return result
