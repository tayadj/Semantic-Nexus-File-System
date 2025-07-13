import torch









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