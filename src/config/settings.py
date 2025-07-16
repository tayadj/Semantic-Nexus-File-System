import os
import pydantic
import pydantic_settings



class TokenizerConfig(pydantic.BaseModel):

	vocabulary: str = pydantic.Field(..., description = "Tokenizer vocabulary storage path")
	merges: str = pydantic.Field(..., description = "Tokenizer merges storage path")

class VectorizerConfig(pydantic.BaseModel):

	model: str = pydantic.Field(..., description = "Vectorizer model path")
	data: str = pydantic.Field(..., description = "Vectorizer data path")

class SentifierConfig(pydantic.BaseModel):

	model: str = pydantic.Field(..., description = "Sentifier model path")
	data: str = pydantic.Field(..., description = "Sentifier data path")

class EntifierConfig(pydantic.BaseModel):

	model: str = pydantic.Field(..., description = "Entifier model path")
	data: str = pydantic.Field(..., description = "Entifier data path")



class RouterConfig(pydantic.BaseModel):

	model: str = pydantic.Field(..., description = "Router model path")
	data: str = pydantic.Field(..., description = "Router data path")

class ExtractorConfig(pydantic.BaseModel):

	model: str = pydantic.Field(..., description = "Extractor model path")
	data: str = pydantic.Field(..., description = "Extractor data path")	



class SystemConfig(pydantic.BaseModel):

	root: str = pydantic.Field(..., description = "File system root")

	

class Settings(pydantic_settings.BaseSettings):

	tokenizer: TokenizerConfig
	vectorizer: VectorizerConfig
	sentifier: SentifierConfig
	entifier: EntifierConfig

	router: RouterConfig
	extractor: ExtractorConfig

	system: SystemConfig

	device: str = pydantic.Field(..., description = "Application device")

	model_config = pydantic_settings.SettingsConfigDict(
        env_file = os.path.dirname(__file__) + '/.env',
        env_file_encoding = "utf-8",
        env_nested_delimiter = "__",
        case_sensitive = False,
		extra = 'ignore'
    )