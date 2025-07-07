import os
import pandas

import core



corpus_path = os.path.dirname(__file__) + "/storage/corpus.json"
corpus = pandas.read_json(corpus_path, orient = "records")
corpus = corpus["text"].tolist()

engine = core.Engine()
engine.vectorizer.fit(corpus)

print(engine.sentiment.vectorizer.tokenizer.size)

core.nexus.pipelines.train(engine.sentiment, engine.vectorizer, engine.device)

texts = [
	"Good",
	"Terrible",
	"Amazing"
]

for text in texts:

	print(f"{text}: {engine.vectorizer.tokenizer.encode(text.lower())}")

core.nexus.pipelines.inference(engine.sentiment, texts)