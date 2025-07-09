import os
import torch

import core



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



NER_to_index = {
	"O": 0, 
	"B-PERSON": 1, "I-PERSON": 2,
	"B-LOCATION": 3, "I-LOCATION": 4, 
	"B-GEOPOLITICAL": 5, "I-GEOPOLITICAL": 6, 
	"B-TIME": 7, "I-TIME": 8,
	"B-ORGANIZATION": 9, "I-ORGANIZATION": 10,
	"B-EVENT": 11, "I-EVENT": 12,
	"B-NATURAL": 13, "I-NATURAL": 14,
	"B-ARTIFACT": 15, "I-ARTIFACT": 16
}

index_to_NER = {index: tag for tag, index in NER_to_index.items()}
NER_padding_index = len(NER_to_index)
NER_size = len(NER_to_index) + 1

def map_NER(input):

	return [NER_to_index.get(tag, NER_padding_index) for tag in input]

entity_path = os.path.dirname(__file__) + "/storage/entity.json" 
entity = core.nexus.pipelines.data_entifier(entity_path, map_NER)

core.nexus.pipelines.train_entifier(engine.entifier, entity, engine.device)
torch.save(engine.entifier, os.path.dirname(__file__) + "/storage/entifier.pth")


engine.entifier = torch.load(os.path.dirname(__file__) + "/storage/entifier.pth", weights_only = False)

texts = [
	"Alice went to Paris",
	"John lives in Berlin",
	"Mary works since April 2005.",
	"Google is based in Mountain View"
]
core.nexus.pipelines.inference_entifier(engine.entifier, texts, engine.device, index_to_NER)
