from core.nexus import Engine
from core.system import Manager



class Symbiosis:

	def __init__(self, settings):

		self.engine = Engine(settings)
		self.manager = Manager(settings)