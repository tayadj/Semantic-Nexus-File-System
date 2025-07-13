import os
import torch

import config
import core



if __name__ == "__main__":

	settings = config.Settings()
	engine = core.Engine(settings)

	'''
	sentiment_path = os.path.dirname(__file__) + "/storage/sentiment.json" 
	sentiment = core.nexus.pipelines.data_sentifier(sentiment_path)

	core.nexus.pipelines.train_sentifier(engine.sentifier, sentiment, engine.device, engine.vectorizer)

	texts = [
		"I love coffee on rainy mornings.",
		"This traffic jam is so frustrating.",
		"Absolutely delighted with the surprise party!",
		"I'm feeling under the weather today.",
		"What an amazing performance that was.",
		"I can't stand this noise anymore.",
		"The weather is perfect for a walk.",
		"I feel completely let down by this outcome.",
		"Everything turned out better than expected!",
		"I'm so bored right now."
	]
	core.nexus.pipelines.inference_sentifier(engine.sentifier, texts, engine.device, engine.vectorizer)
	'''
	# application = config.Application(engine, settings)






'''
entity_path = os.path.dirname(__file__) + "/storage/entity.json" 
entity = core.nexus.pipelines.data_entifier(entity_path, config.entifier.map_NER)

core.nexus.pipelines.train_entifier(engine.entifier, entity, engine.device)
torch.save(engine.entifier, os.path.dirname(__file__) + "/storage/entifier.pth")

engine.entifier = torch.load(os.path.dirname(__file__) + "/storage/entifier.pth", weights_only = False)

texts = [
	"Alice went to Paris",
	"John lives in Berlin",
	"Mary works since April 2005.",
	"Google is based in Mountain View"
]
core.nexus.pipelines.inference_entifier(engine.entifier, texts, engine.device, config.entifier)
'''

'''
settings = config.Settings()
engine = core.Engine()
engine.vectorizer = torch.load(settings.vectorizer.path, weights_only = False)
engine.sentifier = torch.load(settings.sentifier.path, weights_only = False)
engine.entifier = torch.load(settings.entifier.path, weights_only = False)

def metafy(file):

	sentiment = core.nexus.pipelines.inference_sentifier(engine.sentifier, [file], engine.device)
	entity = core.nexus.pipelines.inference_entifier(engine.entifier, [file], engine.device, config.entifier)

	metafile = {
		"text": file,
		"metadata": {
			"sentiment": sentiment,
			"entity": entity
		}
	}

	return metafile
'''

'''
settings = config.Settings()
engine = core.Engine()

corpus_path = os.path.dirname(__file__) + "/storage/corpus.json"
corpus = core.nexus.pipelines.data_corpus(corpus_path)

# vectorizer = core.nexus.services.vectorizer.Vectorizer(corpus)
vectorizer = torch.load(os.path.dirname(__file__) + "/storage/models/vectorizer.pth", weights_only = False)
engine.vectorizer = vectorizer

model = core.nexus.pipelines.train_vectorizer(engine.vectorizer, corpus, engine.device, iterations = 1000, epochs = 10)
torch.save(model, os.path.dirname(__file__) + "/storage/models/vectorizer.pth")
'''
