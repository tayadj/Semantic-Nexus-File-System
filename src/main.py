import os
import torch

import config
import core


'''
corpus_path = os.path.dirname(__file__) + "/storage/corpus.json"
corpus = core.nexus.pipelines.data_corpus(corpus_path)

engine = core.Engine()
engine.build(corpus)
print(f"Vocabulary size: {engine.vectorizer.tokenizer.size} tokens")



sentiment_path = os.path.dirname(__file__) + "/storage/sentiment.json" 
sentiment = core.nexus.pipelines.data_sentifier(sentiment_path)

core.nexus.pipelines.train_sentifier(engine.sentifier, sentiment, engine.device)
torch.save(engine.sentifier, os.path.dirname(__file__) + "/storage/sentifier.pth")
engine.sentifier = torch.load(os.path.dirname(__file__) + "/storage/sentifier.pth", weights_only = False)

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
core.nexus.pipelines.inference_sentifier(engine.sentifier, texts, engine.device)



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


corpus_path = os.path.dirname(__file__) + "/storage/corpus.json"
corpus = core.nexus.pipelines.data_corpus(corpus_path)

v = core.nexus.services.vectorizer.TransformerVectorizer(corpus)