import os
import pandas

import core



corpus_path = os.path.dirname(__file__) + "/storage/corpus.json"
corpus = pandas.read_json(corpus_path, orient = "records")
corpus = corpus["text"].tolist()

engine = core.Engine()
engine.vectorizer.fit(corpus)

print(f"Vocabulary size: {engine.sentiment.vectorizer.tokenizer.size} tokens")

sentiment_path = os.path.dirname(__file__) + "/storage/sentiment.json" 
sentiment = pandas.read_json(sentiment_path, orient = "records")
sentiment = pandas.DataFrame(
	{
		"input": sentiment["text"],
		"output": sentiment["sentiment"]
	}
)

core.nexus.pipelines.train(engine.sentiment, sentiment, engine.device)

texts = [
	"Good, thank you!",
	"Terrible",
	"Amazing"
]

for text in texts:

	print(f"{text} [{engine.vectorizer.tokenizer.preprocess(text)}]: {engine.vectorizer.tokenizer.encode(engine.vectorizer.tokenizer.preprocess(text))}")

core.nexus.pipelines.inference(engine.sentiment, texts)