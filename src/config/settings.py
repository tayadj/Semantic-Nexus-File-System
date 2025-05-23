import os
import pydantic
import pydantic_settings



class Settings(pydantic_settings.BaseSettings):
	
	model_config = pydantic_settings.SettingsConfigDict(
		env_file = os.path.dirname(__file__) + '/.env',
		env_file_encoding = 'utf-8',
		extra = 'ignore'
	)

	OPENAI_API_KEY: pydantic.SecretStr

	DATA_STORAGE_PREFIX: pydantic.SecretStr
	DATA_STORAGE_POSTFIX: pydantic.SecretStr
	
