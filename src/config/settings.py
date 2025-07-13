import os
import pydantic
import pydantic_settings



class VectorizerConfig(pydantic.BaseModel):

	path: str = pydantic.Field(..., description = "Vectorizer model path")

class SentifierConfig(pydantic.BaseModel):

	path: str = pydantic.Field(..., description = "Sentifier model path")

class EntifierConfig(pydantic.BaseModel):

	path: str = pydantic.Field(..., description = "Entifier model path")



class SystemConfig(pydantic.BaseModel):

	root: str = pydantic.Field(..., description = "File system root")



class Settings(pydantic_settings.BaseSettings):

	vectorizer: VectorizerConfig
	sentifier: SentifierConfig
	entifier: EntifierConfig

	system: SystemConfig

	device: str = pydantic.Field(..., description = "Application device")

	model_config = pydantic_settings.SettingsConfigDict(
        env_file = os.path.dirname(__file__) + '/.env',
        env_file_encoding = "utf-8",
        env_nested_delimiter = "__",
        case_sensitive = False,
		extra = 'ignore'
    )