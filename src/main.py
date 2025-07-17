import json

import config
import core



if __name__ == "__main__":

	settings = config.Settings()

	with open(settings.vectorizer.data, "r", encoding = "utf-8") as file:

		corpus = json.load(file)

	# symbiosis = core.Symbiosis(settings)

	vectorizer = core.nexus.vectorizer.vectorizer.Vectorizer(settings)
	
