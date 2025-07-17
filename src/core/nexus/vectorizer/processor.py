import json
import torch

from core.nexus.vectorizer.vectorizer import Vectorizer
from core.nexus.vectorizer.tokenizer import Tokenizer



class Processor:

	def __init__(self, settings):

		self.settings = settings
		self.device = torch.device(self.settings.device)
		self.model = None

	def save(self):

		torch.save(self.model.state_dict(), self.settings.vectorizer.model)

	def load(self):

		state = torch.load(self.settings.vectorizer.model, map_location = self.device)
		
		self.instance()
		self.model.load_state_dict(state)
		self.model.to(self.device)

	def instance(self, **config: any):

		self.model = Vectorizer(self.settings, **config)
		self.model.to(self.device)

	def data(self) -> list[str]:

		with open(self.settings.vectorizer.data, "r", encoding = "utf-8") as file:

			data = json.load(file)

		return data

	def train(self, data: list[str], **config: any):

		self.model.train()

		epochs = config.get("epochs", 10)
		iterations = config.get("iterations", 1000)
		batch_size = config.get("batch_size", 8)
		learning_rate = config.get("learning_rate", 1e-4)
		number_negatives = config.get("number_negatives", 20)
		alpha = config.get("alpha", 1.0)
		beta = config.get("beta", 1.0)

		dataset = self.model.Dataset(data, self.model.tokenizer, self.model.sequence_length, self.model.masking_rate)
		loader = torch.utils.data.DataLoader(dataset, batch_size = batch_size, shuffle = True, collate_fn = dataset.collate)

		optimizer = torch.optim.AdamW(self.model.parameters(), lr = learning_rate)
		criterion = torch.nn.CrossEntropyLoss(ignore_index = -1)

		for epoch in range(1, epochs + 1):

			total_loss_MLM = 0.0
			total_loss_NCE = 0.0
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

				loss_MLM = criterion(logits, targets)
				#print(loss_MLM.item())

				mask = targets != -1

				if mask.sum() > 0:

					logits_masked = logits[mask]
					positive_indices = targets[mask]

					top_logits, top_indices = logits_masked.topk(number_negatives + 1, dim = 1)
					top_indices = top_indices[:, 1:]

					permutation = torch.randperm(number_negatives, device = self.device)[:number_negatives]
					hard_negatives = top_indices[:, permutation]

					positive_logits = logits_masked.gather(1, positive_indices.unsqueeze(1))
					negative_logits = logits_masked.gather(1, hard_negatives)
					all_logits = torch.cat([positive_logits, negative_logits], dim = 1)

					positive_loss = -torch.nn.functional.logsigmoid(positive_logits).mean()
					negative_loss = -torch.nn.functional.logsigmoid(-negative_logits).sum(dim = 1).mean()
					loss_NCE = positive_loss + negative_loss

				else:

					loss_NCE = torch.tensor(0.0, device = self.device)

				loss = alpha * loss_MLM + beta * loss_NCE
				loss.backward()
				optimizer.step()

				total_loss_MLM += loss_MLM.item()
				total_loss_NCE += loss_NCE.item()
				iteration_counter += 1

			average_loss_MLM = total_loss_MLM / iteration_counter
			average_loss_NCE = total_loss_NCE / iteration_counter
			print(f"Epoch {epoch}/{epochs}, MLM: {average_loss_MLM:.4f}, NCE: {average_loss_NCE:.4f}")

	def inference(self, data: list[str]):

		self.model.eval()

		with torch.no_grad():

			data = self.model.preprocess(data)
			semantic_embeddings, static_embeddings, masking = self.model(data)

		return semantic_embeddings, static_embeddings, masking

