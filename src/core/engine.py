import llama_index
import llama_index.llms.openai
import os

from .services import OntologyProcessor, SearchProcessor



class Engine():

	def __init__(self, data_interface, **config: any):

		if "openai_api_key" in config: 

			os.environ["OPENAI_API_KEY"] = config.pop("openai_api_key")
			self.model = llama_index.llms.openai.OpenAI(model = "gpt-4.1-nano")
			llama_index.core.Settings.llm = self.model

		self.data_interface = data_interface			

		self.ontology_processor = OntologyProcessor()
		self.search_processor = SearchProcessor()

	def setup(self):

		aggregated_ontology = self.data_interface._aggregate_ontology()

		for entity in aggregated_ontology:

			self.ontology_processor.create_entity(entity)

		self.ontology_processor.build()

	async def query(self, query):

		ontology_context = await self.ontology_processor.process(query)
		
		prompt = (
			f"User query: {query}\n"
			f"Relevant information from knowledge database: {ontology_context}\n"
			"Answer:"
		)

		answer = await self.model.acomplete(prompt)

		return answer