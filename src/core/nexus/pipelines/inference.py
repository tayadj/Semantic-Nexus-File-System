import torch



def inference(model, data):

	model.eval()

	with torch.no_grad():

		logits = model(data)
		probabilities = torch.nn.functional.softmax(logits, dim = 1)
		predictions = torch.argmax(probabilities, dim = 1)

	for record, probability, prediction in zip(data, probabilities, predictions):

		print(f"\"{record}\" -> {prediction} ({probability})")