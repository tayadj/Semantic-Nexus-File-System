"""
This module defines configuration models and a dynamic settings loader using
Pydantic and Pydantic-Settings. It supports loading core system settings
and aggregating arbitrary Nexus module configurations (mediators, services,
and tools) from a .env file with nested delimiters.
"""

import os
import pydantic
import pydantic_settings



class NexusConfig(pydantic.BaseModel):
	"""
	Base model for a Nexus module configuration.

	This model allows arbitrary extra fields to be defined per module.
	It serves as a generic container for configuration values of
	mediators, services, or tools.

	Attributes:
		Any extra fields passed during initialization will be stored
		as model attributes.
	"""

	class Config:
		"""
		Pydantic configuration for NexusConfig.

		extra: allow arbitrary fields in the model.
		json_schema_extra: add a description to the generated JSON schema.
		"""

		extra = pydantic.Extra.allow      
		json_schema_extra = {
			"description": "Nexus module configuration"
		}

class SystemConfig(pydantic.BaseModel):
	"""
	Core system configuration.

	Attributes:
		root (str): Filesystem root path for the system.
		device (str): Device type for the system.
	"""

	root: str = pydantic.Field(..., description = "System root")
	device: str = pydantic.Field(..., description = "System device")

class Settings(pydantic_settings.BaseSettings):
	"""
	Primary application settings loader.

	This class reads a .env file, loads core system configuration,
	and dynamically aggregates additional Nexus module configurations
	(mediators, services, tools) based on environment variable prefixes.

	Attributes:
		system (SystemConfig): Loaded system configuration.
		mediators (dict[str, NexusConfig]): Mapping of mediator names to their configs.
		services (dict[str, NexusConfig]): Mapping of service names to their configs.
		tools (dict[str, NexusConfig]): Mapping of tool names to their configs.
	"""

	system: SystemConfig

	mediators: dict[str, NexusConfig] = {}
	services: dict[str, NexusConfig] = {}
	tools: dict[str, NexusConfig] = {}

	class Config:
		"""
		Pydantic-Settings configuration.

		env_file: Path to the .env file.
		env_file_encoding: Encoding for reading the .env file.
		env_nested_delimiter: Delimiter for nested env variables.
		case_sensitive: Whether keys are case-sensitive.
		extra: Ignore unknown environment variables.
		"""

		env_file = os.path.dirname(__file__) + '/.env'
		env_file_encoding = "utf-8"
		env_nested_delimiter = "___"
		case_sensitive = False
		extra = pydantic.Extra.ignore

	def __init__(self, **kwargs: any):
		"""
		Initialize Settings instance and aggregate module configs.

		Loads environment variables from the configured .env file,
		then populates the mediators, services, and tools dictionaries
		by extracting prefixed variables and instantiating NexusConfig
		for each module.
		"""

		super().__init__(**kwargs)

		variables = self.environment(self.Config.env_file, self.Config.env_file_encoding)

		self.mediators = self.aggregate("MEDIATORS", variables)
		self.services = self.aggregate("SERVICES", variables)
		self.tools = self.aggregate("TOOLS", variables)

	def environment(self, path: str, encoding: str) -> dict[str, str]:
		"""
		Read a .env file and parse simple KEY=VALUE pairs.

		Lines starting with '#' or lacking '=' are skipped.
		Surrounding quotes around values are stripped.

		Args:
			path (str): Filesystem path to the .env file.
			encoding (str): Encoding to use when opening the file.

		Returns:
			dict[str, str]: Mapping of environment variable names to values.
		"""

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
		"""
		Extract and group environment variables by module prefix.

		Looks for variables starting with '{PREFIX}___', splits the key
		into module and field components, and collects values under
		module-specific dictionaries. Then instantiates a NexusConfig
		for each module.

		Args:
			prefix (str): Prefix to filter variables (e.g., "MEDIATORS").
			variables (dict[str, str]): Flat mapping of all env variables.

		Returns:
			dict[str, NexusConfig]: Mapping of module names (lowercased)
			to their NexusConfig instances.
		"""

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
