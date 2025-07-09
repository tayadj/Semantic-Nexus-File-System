import os
import pandas

import core



engine = core.Engine()

corpus_path = os.path.dirname(__file__) + "/storage/corpus.json"
corpus = pandas.read_json(corpus_path, orient = "records")
corpus = corpus["text"].tolist()
engine.build(corpus)

print(f"Vocabulary size: {engine.sentifier.vectorizer.tokenizer.size} tokens")

sentiment_path = os.path.dirname(__file__) + "/storage/sentiment.json" 
sentiment = pandas.read_json(sentiment_path, orient = "records")
sentiment = pandas.DataFrame(
	{
		"input": sentiment["text"],
		"output": sentiment["sentiment"]
	}
)

core.nexus.pipelines.train_sentifier(engine.sentifier, sentiment, engine.device)

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

for text in texts:

	print(f"{text} [{engine.vectorizer.tokenizer.preprocess(text)}]: {engine.vectorizer.tokenizer.encode(engine.vectorizer.tokenizer.preprocess(text))}")

core.nexus.pipelines.inference_sentifier(engine.sentifier, texts, engine.device)

NER_to_index = {"O": 0, "B-PERSON": 1, "I-PERSON": 2, "B-LOCATION": 3, "I-LOCATION": 4, "B-TIME": 5, "I-TIME": 6}
index_to_NER = {index: tag for tag, index in NER_to_index.items()}
NER_padding_index = len(NER_to_index)
NER_size = len(NER_to_index) + 1

def map_NER(input):

    return [NER_to_index.get(tag, NER_padding_index) for tag in input]

entity_path = os.path.dirname(__file__) + "/storage/entity.json" 
entity = pandas.read_json(entity_path, orient = "records")
entity["entity"] = entity["entity"].apply(map_NER)
entity = pandas.DataFrame(
	{
		"input": entity["text"],
		"output": entity["entity"]
	}
)

core.nexus.pipelines.train_entifier(engine.entifier, entity, engine.device)

texts = [
    "Alice went to Paris",
    "John lives in Berlin",
    "Mary works since April 2005.",
    "Google is based in Mountain View"
]

core.nexus.pipelines.inference_entifier(engine.entifier, texts, engine.device, index_to_NER)
