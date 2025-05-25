import llama_index



class OntologyProcessor:

	def __init__(self):

		self.index = None
		self.query_engine = None

	def build(self, ontology):

		self.index = llama_index.core.indices.knowledge_graph.KnowledgeGraphIndex([], llm = llama_index.core.Settings.llm)

		for entity in ontology:

			triplet = (entity["head"], entity["relation"], entity["tail"])
			self.index.upsert_triplet(triplet, include_embeddings = False)

	async def process(self, query):

		if not self.index:

			raise ValueError("Knowledge Graph Index hasn't built yet.")

		if not self.query_engine:

			self.query_engine = self.index.as_query_engine(include_text = True, response_mode = "tree_summarize")

		results = await self.query_engine.aquery(query)

		return results
