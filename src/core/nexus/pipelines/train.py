import torch



sentiment_texts = [
    "Good",
    "Very good",
    "Amazing",
    "Really cool",
    "Excellent",
    "Awesome",
    "I loved it",
    "It was fantastic",
    "Best experience ever",
    "So nice",
    "Great service",
    "Superb",
    "Absolutely loved it",
    "Pleasant surprise",
    "Highly recommend",
    "Delightful",
    "Impressive work",
    "Perfectly done",
    "Wonderful time",
    "Incredible job",
    "Not bad",
    "Could be better",
    "It's okay",
    "Mediocre",
    "I don't like it",
    "It was terrible",
    "Awful",
    "Really bad",
    "Worst ever",
    "Not good",
    "Boring",
    "Disappointing",
    "Nothing special",
    "Meh",
    "Horrible",
    "Waste of time",
    "Would not recommend",
    "So disappointing",
    "Frustrating experience",
    "Terribly executed",
    "Fantastic quality",
    "Very helpful",
    "Loved every moment",
    "Truly satisfying",
    "Worth every penny",
    "Bright and uplifting",
    "So grateful",
    "Completely satisfied",
    "Just perfect",
    "Spectacular"
    "Thank you!"
]

sentiment_labels = [
    1, 1, 1, 1, 1,
    1, 1, 1, 1, 1,
    1, 1, 1, 1, 1,
    1, 1, 1, 1, 1,
    0, 0, 0, 0, 0,
    0, 0, 0, 0, 0,
    0, 0, 0, 0, 0,
    0, 0, 0, 0, 0,
    1, 1, 1, 1, 1,
    1, 1, 1, 1, 1,
    1
]



def train(model, device):

	model.to(device)

	dataset = model.Dataset(sentiment_texts, sentiment_labels)
	loader = torch.utils.data.DataLoader(dataset, batch_size = 2, shuffle = True, collate_fn = dataset.collate)

	optimizer = torch.optim.Adam(model.parameters(), lr = 1e-3)
	criterion = torch.nn.CrossEntropyLoss()

	model.train()
	epochs = 10

	for epoch in range(1, epochs + 1):

		total_loss = 0.0

		for texts, labels in loader:

			logits = model(texts)
			loss = criterion(logits, labels.to(device))

			optimizer.zero_grad()
			loss.backward()
			optimizer.step()

			total_loss += loss.item()

		average_loss = total_loss / len(loader)

		print(f"Epoch {epoch:02d}/{epochs}, Loss: {average_loss:.4f}")

	return model