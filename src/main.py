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

core.nexus.pipelines.train(engine.sentifier, sentiment, engine.device)

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

core.nexus.pipelines.inference(engine.sentifier, texts, engine.device)
