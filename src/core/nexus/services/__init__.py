import importlib
import pathlib



services = {}

for entry in pathlib.Path(__file__).parent.iterdir():

	if entry.is_dir():

		service = entry.name
		module = importlib.import_module(f"{__package__}.{service}")
		instance = getattr(module, "Processor", None)

		if instance:

			services[service] = instance