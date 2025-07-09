import pandas



def data_corpus(path):

	corpus = pandas.read_json(path, orient = "records")
	corpus = corpus["text"].tolist()

	return corpus

def data_sentifier(path):

	sentiment = pandas.read_json(path, orient = "records")
	sentiment = pandas.DataFrame(
		{
			"input": sentiment["text"],
			"output": sentiment["sentiment"]
		}
	)

	return sentiment

def data_entifier(path, mapping):

	entity = pandas.read_json(path, orient = "records")
	entity["entity"] = entity["entity"].apply(mapping)
	entity = pandas.DataFrame(
		{
			"input": entity["text"],
			"output": entity["entity"]
		}
	)

	return entity