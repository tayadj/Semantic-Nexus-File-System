import config
import core



if __name__ == "__main__":

	settings = config.Settings()
	symbiosis = core.Symbiosis(settings)

	tokenizer = core.nexus.vectorizer.Tokenizer(settings)
	corpus = symbiosis.engine.services["vectorizer"].data()
	
