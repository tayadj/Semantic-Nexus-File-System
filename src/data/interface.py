import base64
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

	def build_metafile(self, path):

		_, extension = os.path.splitext(path)
		extension = extension.lower()

		with open(path, "rb") as file:

			data = file.read()

		for rule in self.mapping:

			if extension in rule["extensions"]:

				text, image, audio, video = rule["handler"](data)

		ontology = self.build_ontology(text)

		metafile = mediator.Metafile(
			text = text,
			image = image,
			audio = audio,
			video = video,
			ontology = ontology
		)

		return metafile

	def handle_text(self, text):

		text = text.decode("utf-8", errors = "ignore")

		return (text, None, None, None)

	def handle_image(self, image):

		text = ""

		return (text, image, None, None)

	def handle_audio(self, audio):

		text = ""

		return (text, None, audio, None)

	def handle_video(self, video):

		text = ""

		return (text, None, None, video)

	def build_ontology(self, text):

		pass
	
	def _create_file(self, id, metafile):

		mediator.create_file(f"{self.data_storage_prefix}/{id}{self.data_storage_postfix}", metafile)

	def _read_file(self, id):

		return mediator.read_file(f"{self.data_storage_prefix}/{id}{self.data_storage_postfix}")

	def _delete_file(self, id):
		
		mediator.delete_file(f"{self.data_storage_prefix}/{id}{self.data_storage_postfix}")

