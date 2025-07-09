import torch



def train_sentifier(model, data, device):

	model.to(device)
	model.train()

	dataset = model.Dataset(data["input"].tolist(), data["output"].tolist())
	loader = torch.utils.data.DataLoader(dataset, batch_size = 2, shuffle = True, collate_fn = dataset.collate)

	optimizer = torch.optim.Adam(model.parameters(), lr = 1e-3)
	criterion = torch.nn.CrossEntropyLoss()

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



def train_entifier(model, data, device):

	model.to(device)
	model.train()

	dataset = model.Dataset(data["input"].tolist(), data["output"].tolist())
	loader = torch.utils.data.DataLoader(dataset, batch_size = 2, shuffle = True, collate_fn = dataset.collate)

	optimizer = torch.optim.Adam(model.parameters(), lr = 1e-3)
	criterion = torch.nn.CrossEntropyLoss(ignore_index = 17) # NER_padding_index

	epochs = 10

	for epoch in range(1, epochs + 1):

		total_loss = 0.0

		count = 0 # to remove for full-training

		for texts, labels in loader:

			count += 1
			if count == 1000:

				break

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

				pass
				# print(exception, '\n', texts, labels, "\n\n\n")

		average_loss = total_loss / 1000 # len(loader)

		print(f"Epoch {epoch:02d}/{epochs}, Loss: {average_loss:.4f}")

	return model