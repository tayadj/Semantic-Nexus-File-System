import torch


# To Remove
'''
def train_vectorizer(model, corpus, device, epochs = 10, iterations = 100):

	model.to(device)
	model.train()

	dataset = model.Dataset(corpus, model.tokenizer, model.sequence_length, model.masking_rate)
	loader = torch.utils.data.DataLoader(dataset, batch_size = 8, shuffle = True, collate_fn = dataset.collate)

	optimizer = torch.optim.AdamW(model.parameters(), lr = 5e-3)
	criterion = torch.nn.CrossEntropyLoss(ignore_index = -1)

	for epoch in range(1, epochs + 1):

		total_loss = 0.0

		counter = 0

		for indices, labels in loader:

			counter += 1

			if counter > iterations:

				break

			labels = labels.to(device)
			indices = indices.to(device)

			optimizer.zero_grad()

			semantic_embeddings, static_embeddings, output = model(indices)
			logits = output.view(-1,  output.size(-1))
			targets = labels.view(-1)
			loss = criterion(logits, targets)
			loss.backward()

			optimizer.step()

			total_loss += loss.item()

		average_loss = total_loss / (counter - 1)

		print(f"Epoch {epoch:02d}/{epochs}, Loss: {average_loss:.4f}")
		torch.save(model, f"vectorizer_epoch_{epoch:02d}.pth")

	return model
'''

# To Remove
'''
def train_sentifier(model, data, device, vectorizer):

	model.to(device)
	model.train()

	vectorizer.to(device)
	vectorizer.eval()

	dataset = model.Dataset(data["input"].tolist(), data["output"].tolist(), vectorizer)
	loader = torch.utils.data.DataLoader(dataset, batch_size = 2, shuffle = True, collate_fn = dataset.collate)

	optimizer = torch.optim.Adam(model.parameters(), lr = 1e-3)
	criterion = torch.nn.CrossEntropyLoss()

	epochs = 10

	for epoch in range(1, epochs + 1):

		total_loss = 0.0

		for embeddings, labels in loader:

			embeddings = embeddings.to(device)
			labels = labels.to(device)

			logits = model(embeddings)
			loss = criterion(logits, labels)

			optimizer.zero_grad()
			loss.backward()
			optimizer.step()

			total_loss += loss.item()

		average_loss = total_loss / len(loader)

		print(f"Epoch {epoch:02d}/{epochs}, Loss: {average_loss:.4f}")

	return model
'''








'''
def train_entifier(model, data, device):

	model.to(device)
	model.train()

	dataset = model.Dataset(data["input"].tolist(), data["output"].tolist())
	loader = torch.utils.data.DataLoader(dataset, batch_size = 8, shuffle = True, collate_fn = dataset.collate)

	optimizer = torch.optim.Adam(model.parameters(), lr = 1e-3)
	criterion = torch.nn.CrossEntropyLoss(ignore_index = 17) # NER_padding_index

	epochs = 1

	for epoch in range(1, epochs + 1):

		total_loss = 0.0

		err_counter = 0

		for texts, labels in loader:

			try:

				labels = labels.to(device)
				logits = model(texts).to(device)

				batch, layer, channel = logits.shape
				logits = logits.view(-1, channel)
				labels = labels.view(-1)

				loss = criterion(logits, labels)

				optimizer.zero_grad()
				loss.backward()
				optimizer.step()

				total_loss += loss.item()

			except Exception as exception:

				err_counter += 8 # batch_size

		average_loss = total_loss / (len(loader) - err_counter) 

		print(f"Epoch {epoch:02d}/{epochs}, Loss: {average_loss:.4f}")

	return model
'''