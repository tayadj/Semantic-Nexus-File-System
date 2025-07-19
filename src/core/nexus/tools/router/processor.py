import json
import torch

from core.nexus.tools.router.router import Router
from core.nexus.mediators.textual import Processor as Vectorizer



class Processor:

	def __init__(self, settings):

		self.settings = settings
		self.device = torch.device(self.settings.system.device)
		self.model = None

		self.vectorizer = Vectorizer(settings)
		self.vectorizer.load()

	def save(self):

		torch.save(self.model.state_dict(), self.settings.tools["router"].model)

	def load(self):

		state = torch.load(self.settings.tools["router"].model, map_location = self.device)
		
		self.instance()
		self.model.load_state_dict(state)
		self.model.to(self.device)

	def instance(self, **config: any):

		self.model = Router(**config)
		self.model.to(self.device)

	def data(self) -> tuple[list[str], list[str]]:

		with open(self.settings.tools["router"].data, "r", encoding = "utf-8") as file:

			data = json.load(file)

		texts, labels = zip(*data)

		return list(texts), list(labels)

	def train(self, data: tuple[list[str], list[str]], **config: any):

		self.model.train()

		epochs = config.get("epochs", 10)
		iterations = config.get("iterations", 1000)
		batch_size = config.get("batch_size", 2)
		learning_rate = config.get("learning_rate", 1e-3)

		dataset = self.model.Dataset(data[0], data[1], self.vectorizer, self.model.operation_to_index)
		loader = torch.utils.data.DataLoader(dataset, batch_size = batch_size, shuffle = True, collate_fn = dataset.collate)

		optimizer = torch.optim.Adam(self.model.parameters(), lr = learning_rate)
		criterion = torch.nn.CrossEntropyLoss(ignore_index = self.model.operation_undefined)

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

			_, _, _, embeddings = self.vectorizer.inference(data)
			logits = self.model(embeddings)
			probabilities = torch.nn.functional.softmax(logits, dim = 1)
			predictions = torch.argmax(probabilities, dim = 1)

		result = [self.model.index_to_operation.get(int(prediction), "undefined") for prediction in predictions]

		return result

		