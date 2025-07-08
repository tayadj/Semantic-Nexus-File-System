import torch



def inference_sentifier(model, data, device):

	model.to(device)
	model.eval()

	with torch.no_grad():

		logits = model(data)
		probabilities = torch.nn.functional.softmax(logits, dim = 1)
		predictions = torch.argmax(probabilities, dim = 1)

	for record, probability, prediction in zip(data, probabilities, predictions):

		print(f"\"{record}\" -> {prediction} ({probability})")

def inference_entifier(model, data, device, mapping):

	model.to(device)
	model.eval()

	with torch.no_grad():

		logits = model(data)
		probabilities = torch.nn.functional.softmax(logits, dim = 2)
		predictions = torch.argmax(probabilities, dim = 2)

	for record, probability, prediction in zip(data, probabilities, predictions):

		prediction = prediction[:len(model.vectorizer.tokenizer.tokenize(record))]
		tags = [mapping[int(index)] for index in prediction]

		print(f"\"{record}\" -> {tags}")

