import json
import torch

from core.nexus.tools.extractor.extractor import Extractor
from core.nexus.mediators.textual import Processor as Vectorizer



class Processor:

	def __init__(self, settings):

		self.settings = settings
		self.device = torch.device(self.settings.device)
		self.model = None

		self.vectorizer = Vectorizer(settings)
		self.vectorizer.load()

	def save(self):

		torch.save(self.model.state_dict(), self.settings.extractor.model)

	def load(self):

		state = torch.load(self.settings.extractor.model, map_location = self.device)
		
		self.instance()
		self.model.load_state_dict(state)
		self.model.to(self.device)

	def instance(self, **config: any):

		self.model = Extractor(**config)
		self.model.to(self.device)

	def data(self) -> tuple[list[list[str]], list[list[str]]]:

		with open(self.settings.extractor.data, "r", encoding = "utf-8") as file:

			data = json.load(file)

		texts, labels = zip(*data)

		return list(texts), list(labels)

	def train(self, data: tuple[list[str], list[list[str]]], **config: any):

		self.model.train()

		epochs = config.get("epochs", 10)
		iterations = config.get("iterations", 1000)
		batch_size = config.get("batch_size", 8)
		learning_rate = config.get("learning_rate", 1e-3)

		dataset = self.model.Dataset(data[0], data[1], self.vectorizer, self.model.tag_to_index)
		loader = torch.utils.data.DataLoader(dataset, batch_size = batch_size, shuffle = True, collate_fn = dataset.collate)

		optimizer = torch.optim.Adam(self.model.parameters(), lr = learning_rate)
		criterion = torch.nn.CrossEntropyLoss(ignore_index = self.model.tag_padding_index)

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
				logits = output.view(-1, output.shape[2])
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

			_, _, _, embeddings = self.vectorizer.inference(data)
			logits = self.model(embeddings)
			probabilities = torch.nn.functional.softmax(logits, dim = 2)
			predictions = torch.argmax(probabilities, dim = 2)

		result = []
		data = self.vectorizer.model.preprocess(data)

		for record, prediction in zip(data, predictions):

			record = [int(index) for index in list(record)]
			decoded_record = [self.vectorizer.model.tokenizer.index_to_token[index] for index in record]

			prediction = [int(index) for index in list(prediction)]
			decoded_prediction = [self.model.index_to_tag.get(index, "<--|PADDING|-->") for index in prediction] 

			current_entity = ""
			current_category = ""

			record_result = []

			for token, tag in zip(decoded_record[1:], decoded_prediction[1:]):

				if token == self.vectorizer.model.tokenizer.token_padding:

					if current_entity:

						record_result.append(current_entity)
						current_entity = ""
						current_category = ""

					break

				if tag.startswith("B-"):

					if current_entity:

						record_result.append(current_entity)
						current_entity = ""
						current_category = ""

					current_entity = token
					current_category = tag[2:]

				elif tag.startswith("I-") and current_category == tag[2:]:

					current_entity += token

				else:

					if current_entity:

						if token == " ":

							current_entity += " "

						else:

							record_result.append(current_entity)
							current_entity = ""
							current_category = ""

			result.append(record_result)

		return result