import torch

def inference_vectorizer(model, data, device):

	model.to(device)
	model.eval()

	with torch.no_grad():

	    embeddings, logits = model(data)

	return {record: embedding for record, embedding in zip(data, embeddings)}


def inference_sentifier(model, data, device, vectorizer):

	model.to(device)
	model.eval()

	vectorizer.to(device)
	vectorizer.eval()

	with torch.no_grad():

		hidden, _ = vectorizer(data)
		embeddings = hidden[:, 0, :]
		logits = model(embeddings)
		probabilities = torch.nn.functional.softmax(logits, dim = 1)
		predictions = torch.argmax(probabilities, dim = 1)

	for record, probability, prediction in zip(data, probabilities, predictions):

		print(f"\"{record}\" -> {prediction} ({probability})")

	return "Positive" if int(prediction) else "Negative"

def inference_entifier(model, data, device, config):

	model.to(device)
	model.eval()

	with torch.no_grad():

		logits = model(data)
		probabilities = torch.nn.functional.softmax(logits, dim = 2)
		predictions = torch.argmax(probabilities, dim = 2)

	for record, probability, prediction in zip(data, probabilities, predictions):

		prediction = prediction[:len(model.vectorizer.tokenizer.tokenize(record))]
		tags = [config.index_to_NER.get(int(index), "<PAD>") for index in prediction]

		print(f"\"{record}\" -> {tags}")

	return tags # last one

