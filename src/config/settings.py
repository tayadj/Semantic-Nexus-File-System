import os
import pydantic
import pydantic_settings



class NexusConfig(pydantic.BaseModel):

	class Config:

		extra = pydantic.Extra.allow      
		json_schema_extra = {
			"description": "Nexus module configuration"
		}

class SystemConfig(pydantic.BaseModel):

	root: str = pydantic.Field(..., description = "System root")
	device: str = pydantic.Field(..., description = "System device")

class Settings(pydantic_settings.BaseSettings):

	system: SystemConfig

	mediators: dict[str, NexusConfig] = {}
	services: dict[str, NexusConfig] = {}
	tools: dict[str, NexusConfig] = {}

	class Config:

		env_file = os.path.dirname(__file__) + '/.env'
		env_file_encoding = "utf-8"
		env_nested_delimiter = "___"
		case_sensitive = False
		extra = pydantic.Extra.ignore

	def __init__(self, **kwargs: any):

		super().__init__(**kwargs)

		variables = self.environment(self.Config.env_file, self.Config.env_file_encoding)

		self.mediators = self.aggregate("MEDIATORS", variables)
		self.services = self.aggregate("SERVICES", variables)
		self.tools = self.aggregate("TOOLS", variables)

	def environment(self, path: str, encoding: str) -> dict[str, str]:

		variables = {}

		with open(path, encoding = encoding) as file:

			for raw in file:

				line = raw.strip()

				if not line or line.startswith("#") or "=" not in line:

					continue

				key, value = line.split("=", maxsplit = 1)
				key = key.strip()
				value = value.strip().strip("'").strip("\"")

				variables[key] = value

		return variables
	
	def aggregate(self, prefix: str, variables: dict[str, str]) -> dict[str, NexusConfig]:

		bucket = {}

		for key, value in variables.items():

			if not key.startswith(prefix + self.Config.env_nested_delimiter):

				continue

			_, module, field = key.split(self.Config.env_nested_delimiter, maxsplit = 2)
			bucket.setdefault(module.lower(), {})[field.lower()] = value

		return {
			module : NexusConfig(**configuration)
			for module, configuration in bucket.items()
		}
