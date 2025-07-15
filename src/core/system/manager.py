import inspect
import pathlib

from core.system.architecture.objects import Node
from core.system.architecture.operations import operations




class Manager:

	def __init__(self, settings):

		self.settings = settings
		self.operations = { operation : instance for operation, instance in operations.items() }

	def __getattr__(self, operation: str):

		instance = self.operations.get(operation)

		if instance is None:

			raise AttributeError(f"{self.__class__.__name__} has no operation {operation}")

		signature = inspect.signature(instance.__init__)
		arguments = list(signature.parameters.values())[1:]	
		wrapper_arguments = []

		for argument in arguments:

			if argument.name == "data":

				wrapper_arguments.append(argument)
				wrapper_arguments.append(
					inspect.Parameter(
						"metadata",
						kind = inspect.Parameter.POSITIONAL_OR_KEYWORD,
						annotation = dict
					)	
				)

			else:

				wrapper_arguments.append(argument)

		wrapper_signature = signature.replace(parameters = wrapper_arguments)

		def wrapper(*args, **kwargs):

			bound = wrapper_signature.bind_partial(*args, **kwargs)
			operation_kwargs = {}

			if "uri" in bound.arguments:

				uri = bound.arguments["uri"]
				uri = pathlib.Path(f"{self.settings.system.root}/{uri}.meta")
				operation_kwargs["uri"] = uri

			if "data" in bound.arguments:

				data = bound.arguments["data"]
				metadata = bound.arguments["metadata"]
				blob = Node(operation_kwargs["uri"], data.encode(), metadata).serialize()
				operation_kwargs["data"] = blob

			operation = instance(**operation_kwargs)
				
			try:

				result = operation.execute()

				if isinstance(result, bytes):

					node = Node()
					node.deserialize(result)
                   
					return node

				else:

					return result

			except Exception as exception:

				print(f"Oops! {exception}")
				operation.rollback()

		wrapper.__signature__ = wrapper_signature

		return wrapper
