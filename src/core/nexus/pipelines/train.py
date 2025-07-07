import torch



sentiment_texts = [
	"very bad",
	"amazing",
	"terrible service",
	"I love this product",
	"worst experience ever",
	"best purchase I've made",
	"I hate it",
	"highly recommend",
	"not worth the money",
	"absolutely fantastic",
	"very disappointing",
	"exceeded my expectations",
	"I will never buy this again",
	"superb quality",
	"it's awful",
	"I'm so happy with this",
	"complete waste",
	"incredible value",
	"not as described",
	"truly enjoyable",
	"thrilled by the efficiency of this tool",
	"extremely disappointed with the outcome"
]

sentiment_labels = [
	0,  
	1,  
	0,  
	1,  
	0,  
	1, 
	0,  
	1,  
	0,  
	1,  
	0,  
	1,  
	0,  
	1,  
	0, 
	1, 
	0, 
	1,  
	0, 
	1, 
	1,
	0
]

def train(model, vectorizer, device):

	model.to(device)

	dataset = model.Dataset(sentiment_texts, sentiment_labels, vectorizer.tokenizer)
	loader = torch.utils.data.DataLoader(dataset, batch_size = 2, shuffle = True, collate_fn = dataset.collate)

	optimizer = torch.optim.Adam(model.parameters(), lr = 1e-3)
	criterion = torch.nn.CrossEntropyLoss()

	model.train()
	epochs = 10

	for epoch in range(1, epochs + 1):

		total_loss = 0.0

		for indices, labels in loader:

			batch = [
				" ".join(vectorizer.tokenizer.index_to_token[index.item()]
				for index in sequence if index.item() != vectorizer.tokenizer.index_padding)
				for sequence in indices
			]

			logits = model(batch)
			loss = criterion(logits, labels.to(device))

			optimizer.zero_grad()
			loss.backward()
			optimizer.step()
			total_loss += loss.item()

		average_loss = total_loss / len(loader)

		print(f"Epoch {epoch:02d}/{epochs}, Loss: {average_loss:.4f}")

	return model