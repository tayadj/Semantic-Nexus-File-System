import config
import core
import data



if __name__ == "__main__":

	settings = config.Settings()

	engine = core.Engine(
		data.Interface(settings),
		openai_api_key = settings.OPENAI_API_KEY.get_secret_value()
	)
	engine.setup()
