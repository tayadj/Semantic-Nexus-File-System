import torch

# To Remove
'''
def inference_sentifier(model, data, device, vectorizer):

	model.to(device)
	model.eval()

	vectorizer.to(device)
	vectorizer.eval()

	with torch.no_grad():

		_, static_embeddings, _ = vectorizer(vectorizer.preprocess(data))
		logits = model(static_embeddings)
		probabilities = torch.nn.functional.softmax(logits, dim = 1)
		predictions = torch.argmax(probabilities, dim = 1)

	for record, probability, prediction in zip(data, probabilities, predictions):

		print(f"\"{record}\" -> {prediction} ({probability})")
'''



'''
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
'''
