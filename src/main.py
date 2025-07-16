import config
import core



if __name__ == "__main__":

	settings = config.Settings()
	symbiosis = core.Symbiosis(settings)

	corpus = symbiosis.engine.services["vectorizer"].data()

	processor = core.nexus.vectorizer.Processor(settings)
	processor.instance(settings)
	
