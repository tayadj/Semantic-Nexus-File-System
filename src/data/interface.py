from . import mediator


class Interface:

	def __init__(self, settings):

		self.settings = settings

	def create_file(self, id, metafile):

		mediator.create_file(f"{self.settings.DATA_STORAGE_PREFIX.get_secret_value()}/{id}{self.settings.DATA_STORAGE_POSTFIX.get_secret_value()}")

	def read_file(self, id):

		return mediator.read_file(f"{self.settings.DATA_STORAGE_PREFIX.get_secret_value()}/{id}{self.settings.DATA_STORAGE_POSTFIX.get_secret_value()}")

	def delete_file(self, id):
		
		mediator.delete_file(f"{self.settings.DATA_STORAGE_PREFIX.get_secret_value()}/{id}{self.settings.DATA_STORAGE_POSTFIX.get_secret_value()}")

