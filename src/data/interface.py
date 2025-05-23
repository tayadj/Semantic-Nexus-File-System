import base64
import llama_index
import os

from . import mediator


class Interface:

	def __init__(self, settings):

		self.data_storage_prefix = settings.DATA_STORAGE_PREFIX.get_secret_value()
		self.data_storage_postfix = settings.DATA_STORAGE_POSTFIX.get_secret_value()

		self.mapping = [
			{
				"extensions": (".txt", ".md"),
				"handler": self.handle_text
			},
			{
				"extensions": (".jpg", ".jpeg", ".png"),
				"handler": self.handle_image
			},
			{
				"extensions": (".mp3"),
				"handler": self.handle_audio
			},
			{
				"extensions": (".mp4"),
				"handler": self.handle_video
			}
		]

		self.ontology_prompt = llama_index.core.prompts.PromptTemplate(
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

	async def build_metafile(self, path):

		_, extension = os.path.splitext(path)
		extension = extension.lower()

		with open(path, "rb") as file:

			data = file.read()

		for rule in self.mapping:

			if extension in rule["extensions"]:

				text, image, audio, video = await rule["handler"](data)

		ontology = await self.build_ontology(text)

		metafile = mediator.Metafile(
			text = text,
			image = image,
			audio = audio,
			video = video,
			ontology = ontology
		)

		return metafile

	async def handle_text(self, text):

		text = text.decode("utf-8", errors = "ignore")

		return (text, None, None, None)

	async def handle_image(self, image):

		text = ""

		return (text, image, None, None)

	async def handle_audio(self, audio):

		text = ""

		return (text, None, audio, None)

	async def handle_video(self, video):

		text = ""

		return (text, None, None, video)

	async def build_ontology(self, text):

		result = await (
			llama_index.core.Settings.llm
				.acomplete(self.ontology_prompt.format(context = text))		
		)

		return json.loads(str(result))
	
	def _create_file(self, id, metafile):

		mediator.create_file(f"{self.data_storage_prefix}/{id}{self.data_storage_postfix}", metafile)

	def _read_file(self, id):

		return mediator.read_file(f"{self.data_storage_prefix}/{id}{self.data_storage_postfix}")

	def _delete_file(self, id):
		
		mediator.delete_file(f"{self.data_storage_prefix}/{id}{self.data_storage_postfix}")

