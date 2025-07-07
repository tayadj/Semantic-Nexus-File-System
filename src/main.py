import os
import pandas

import core



corpus_path = os.path.dirname(__file__) + "/storage/corpus.json"
corpus = pandas.read_json(corpus_path, orient = "records")
corpus = corpus["text"].tolist()

engine = core.Engine()
engine.vectorizer.fit(corpus)

print(engine.sentiment.vectorizer.tokenizer.size)

core.nexus.pipelines.train(engine.sentiment, engine.device)

texts = [
	"Good, thank you!",
	"Terrible",
	"Amazing"
]

for text in texts:

	print(f"{text} [{engine.vectorizer.tokenizer.preprocess(text)}]: {engine.vectorizer.tokenizer.encode(engine.vectorizer.tokenizer.preprocess(text))}")

core.nexus.pipelines.inference(engine.sentiment, texts)