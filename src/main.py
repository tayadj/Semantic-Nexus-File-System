import json

import config
import core



if __name__ == "__main__":

	settings = config.Settings()
	# symbiosis = core.Symbiosis(settings)

	vectorizer = core.nexus.vectorizer.vectorizer["vectorizer"](settings)
	
