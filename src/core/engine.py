import llama_index
import llama_index.llms.openai
import os

from .services import OntologyProcessor



class Engine():

	def __init__(self, **config: any):

		if 'openai_api_key' in config: 

			os.environ['OPENAI_API_KEY'] = config.pop('openai_api_key')

			self.model = llama_index.llms.openai.OpenAI(model = 'gpt-4.1-nano')
			llama_index.core.Settings.llm = self.model

		self.ontology_processor = OntologyProcessor()
