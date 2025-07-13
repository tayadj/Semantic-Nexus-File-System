import pandas



def data_corpus(path):

	corpus = pandas.read_json(path, orient = "records")

	return corpus["text"].tolist()

def data_sentifier(path):

	sentiment = pandas.read_json(path, orient = "records")

	return (sentiment["text"].tolist(), sentiment["sentiment"].tolist())

def data_entifier(path):

	entity = pandas.read_json(path, orient = "records")

	return (entity["text"].tolist(), entity["entity"].tolist())