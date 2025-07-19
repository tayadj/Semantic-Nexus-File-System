import importlib
import pathlib



mediators = {}

for entry in pathlib.Path(__file__).parent.iterdir():

	if entry.is_dir():

		mediator = entry.name
		module = importlib.import_module(f"{__package__}.{mediator}")
		instance = getattr(module, "Processor", None)

		if instance:

			mediators[mediator] = instance