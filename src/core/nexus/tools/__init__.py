import importlib
import pathlib



tools = {}

for entry in pathlib.Path(__file__).parent.iterdir():

	if entry.is_dir():

		tool = entry.name
		module = importlib.import_module(f"{__package__}.{tool}")
		instance = getattr(module, "Processor", None)

		if instance:

			tools[tool] = instance