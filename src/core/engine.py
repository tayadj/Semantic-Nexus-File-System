import llama_index
import llama_index.llms.openai
import os

from .services import OntologyProcessor, SearchProcessor



class Engine():

	def __init__(self, **config: any):

		if 'openai_api_key' in config: 

			os.environ['OPENAI_API_KEY'] = config.pop('openai_api_key')

			self.model = llama_index.llms.openai.OpenAI(model = 'gpt-4.1-nano')
			llama_index.core.Settings.llm = self.model

		self.ontology_processor = OntologyProcessor()
		self.search_processor = SearchProcessor()

	def query(self):

		pass