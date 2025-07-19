import json
import torch

from core.nexus.mediators.textual.vectorizer import Vectorizer
from core.nexus.mediators.textual.tokenizer import Tokenizer



class Processor:

	def __init__(self, settings):

		self.settings = settings
		self.device = torch.device(self.settings.system.device)
		self.model = None

	def save(self):

		torch.save(self.model.state_dict(), self.settings.mediators["textual"].model)

	def load(self):

		state = torch.load(self.settings.mediators["textual"].model, map_location = self.device)
		
		self.instance()
		self.model.load_state_dict(state)
		self.model.to(self.device)

	def instance(self, **config: any):

		self.model = Vectorizer(self.settings, **config)
		self.model.to(self.device)

	def data(self) -> list[str]:

		with open(self.settings.mediators["textual"].data, "r", encoding = "utf-8") as file:

			data = json.load(file)

		return data

	def train(self, data: list[str], **config: any):

		def loss_NCE_(logits: torch.Tensor, targets: torch.Tensor):

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

			return loss_NCE

		def loss_InfoNCE_(first: torch.Tensor, second: torch.Tensor, temperature):

			batch_dimension, layer_dimension, projection_dimension = first.size()

			first_flat = first.view(batch_dimension * layer_dimension, projection_dimension)
			second_flat = second.view(batch_dimension * layer_dimension, projection_dimension)

			aggregated = torch.cat([first_flat, second_flat], dim = 0)
			similarity = torch.matmul(aggregated, aggregated.T) / temperature

			mask = torch.eye(2 * batch_dimension * layer_dimension, device = similarity.device, dtype = torch.bool)
			similarity = similarity.masked_fill(mask, -1e9)

			target = torch.arange(0, 2 * batch_dimension * layer_dimension, device = self.device)
			target = (target + batch_dimension * layer_dimension) % (2 * batch_dimension * layer_dimension)

			loss_InfoNCE = torch.nn.functional.cross_entropy(similarity, target, reduction = "mean")

			return loss_InfoNCE

		self.model.train()

		epochs = config.get("epochs", 10)
		iterations = config.get("iterations", 1000)
		batch_size = config.get("batch_size", 8)
		learning_rate = config.get("learning_rate", 1e-4)
		max_learning_factor = config.get("max_learning_factore", 10)
		warmup_ratio = config.get("warmup_ratio", 0.3)
		number_negatives = config.get("number_negatives", 10)
		alpha = config.get("alpha", 1.0)
		beta = config.get("beta", 1.0)
		gamma = config.get("gamma", 1.0)
		temperature = config.get("temperature", 0.1)

		total_iterations = epochs * iterations
		warmup_iterations = int(total_iterations * warmup_ratio)

		dataset = self.model.Dataset(data, self.model.tokenizer, self.model.sequence_length, self.model.masking_rate)
		loader = torch.utils.data.DataLoader(dataset, batch_size = batch_size, shuffle = True, collate_fn = dataset.collate)

		optimizer = torch.optim.AdamW(self.model.parameters(), lr = learning_rate)
		scheduler = torch.optim.lr_scheduler.OneCycleLR(
			optimizer,
			max_lr = learning_rate * max_learning_factor,
			epochs = epochs,
			steps_per_epoch = iterations,
			pct_start = warmup_ratio,
			anneal_strategy = "cos",
			cycle_momentum = False
		)
		criterion = torch.nn.CrossEntropyLoss(ignore_index = -1)

		for epoch in range(1, epochs + 1):

			total_loss_MLM = 0.0
			total_loss_NCE = 0.0
			total_loss_InfoNCE = 0.0
			iteration_counter = 0

			for indices, labels in loader:

				if iteration_counter == iterations:

					break

				indices = indices.to(self.device)
				labels = labels.to(self.device)

				optimizer.zero_grad()

				_, _, output_first, projection_first = self.model(indices)
				_, _, output_second, projection_second = self.model(indices)
				logits_first = output_first.view(-1,  output_first.size(-1))
				logits_second = output_second.view(-1,  output_second.size(-1))
				targets = labels.view(-1)

				loss_MLM = (criterion(logits_first, targets) + criterion(logits_second, targets)) / 2
				loss_NCE = (loss_NCE_(logits_first, targets) + loss_NCE_(logits_second, targets)) / 2
				loss_InfoNCE = loss_InfoNCE_(projection_first, projection_second, temperature)

				loss = alpha * loss_MLM + beta * loss_NCE + gamma * loss_InfoNCE
				loss.backward()

				optimizer.step()
				scheduler.step()

				total_loss_MLM += loss_MLM.item()
				total_loss_NCE += loss_NCE.item()
				total_loss_InfoNCE += loss_InfoNCE.item()

				iteration_counter += 1

			average_loss_MLM = total_loss_MLM / iteration_counter
			average_loss_NCE = total_loss_NCE / iteration_counter
			average_loss_InfoNCE = total_loss_InfoNCE / iteration_counter
			current_learning_rate = scheduler.get_last_lr()[0]
			print(f"Epoch {epoch}/{epochs}, learning rate = {current_learning_rate:.4f} -> MLM: {average_loss_MLM:.4f}, NCE: {average_loss_NCE:.4f}, InfoNCE: {average_loss_InfoNCE:.4f}")

	def inference(self, data: list[str]):

		self.model.eval()

		with torch.no_grad():

			data = self.model.preprocess(data)
			semantic_embeddings, static_embeddings, masking, projection = self.model(data)

		return semantic_embeddings, static_embeddings, masking, projection

