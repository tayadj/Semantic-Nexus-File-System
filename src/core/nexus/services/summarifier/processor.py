import json
import torch

from core.nexus.services.summarifier.summarifier import Summarifier
from core.nexus.mediators.textual import Processor as Vectorizer



class Processor:

	def __init__(self, settings):

		self.settings = settings
		self.device = torch.device(self.settings.system.device)
		self.model = None

		self.vectorizer = Vectorizer(settings)
		self.vectorizer.load()

	def save(self):

		torch.save(self.model.state_dict(), self.settings.services["summarifier"].model)

	def load(self):

		state = torch.load(self.settings.services["summarifier"].model, map_location = self.device)
		
		self.instance()
		self.model.load_state_dict(state)
		self.model.to(self.device)

	def instance(self, **config: any):

		self.model = Summarifier(**config)
		self.model.to(self.device)

	def data(self) -> tuple[list[str], list[str]]:

		with open(self.settings.services["summarifier"].data, "r", encoding = "utf-8") as file:

			data = json.load(file)

		texts, summaries = zip(*data)

		return list(texts), list(summaries)