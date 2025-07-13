import importlib
import pkgutil



services = {}

for finder, module_name, is_package, in pkgutil.iter_modules(__path__):

	module = importlib.import_module(f"{__name__}.{module_name}")
	service = getattr(module, "Processor", None)

	if service:

		services[module_name] = service