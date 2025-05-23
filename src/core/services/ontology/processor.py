import json
import llama_index



class OntologyProcessor:

	def __init__(self):

		self.prompt = llama_index.core.prompts.PromptTemplate(
			"You are tasked with building an ontology from a provided context (delimited by ```). "
			"Identify atomic key terms (e.g., object, entity, location, organization, person, acronym, concept) in each sentence. "
			"For terms appearing together in a sentence or paragraph, infer one-to-one relationships and explain each briefly.\n"
			"Return your results as a JSON list where each item is an object with:\n"
			"  'head': key term\n"
			"  'relation': relation description\n"
			"  'tail': related term\n"
			"Context: ```{context}```\n"
			"Output: "
		)

	async def process(self, metafile):

		result = await (
			llama_index.core.Settings.llm
				.acomplete(self.prompt.format(context = metafile.text))		
		)
		metafile.ontology = json.loads(str(result))

		return metafile