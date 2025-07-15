import importlib
import pathlib



operations = {}

for entry in pathlib.Path(__file__).parent.iterdir():

	if entry.is_file() and not entry.stem.startswith("_"):

		operation = entry.stem
		module = importlib.import_module(f"{__package__}.{operation}")

		instance_name = "".join(part.capitalize() for part in operation.split("_"))
		instance = getattr(module, instance_name, None)

		if instance:

			operations[operation] = instance
