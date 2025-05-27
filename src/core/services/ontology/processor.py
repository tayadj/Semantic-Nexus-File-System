import llama_index
import networkx



class OntologyProcessor:

	def __init__(self):

		self.graph = networkx.MultiDiGraph()
		self.index = None
		self.query_engine = None

	def create_entity(self, entity: dict):
	
		head = entity.get("head")
		relation = entity.get("relation")
		tail = entity.get("tail")

		if not self.graph.has_node(head):

			self.graph.add_node(head)

		if not self.graph.has_node(tail):

			self.graph.add_node(tail)

		self.graph.add_edge(head, tail, relation = relation)

	def delete_entity(self, entity: dict):

		head = entity.get("head")
		relation = entity.get("relation")
		tail = entity.get("tail")

		if self.graph.has_edge(head, tail):
			
			for key, attributes in self.graph.get_edge_data(head, tail).items():

				if attributes.get("relation") == relation:

					self.graph.remove_edge(head, tail, key = key)	

	def build(self):

		self.index = llama_index.core.indices.knowledge_graph.KnowledgeGraphIndex([], llm = llama_index.core.Settings.llm)

		for head, tail, data in self.graph.edges(data = True):

			triplet = (head, data.get("relation"), tail)
			self.index.upsert_triplet(triplet, include_embeddings = False)

	async def process(self, query):

		if not self.index:

			self.build()
			self.query_engine = self.index.as_query_engine(include_text = True, response_mode = "tree_summarize")

		results = await self.query_engine.aquery(query)

		return results
