import torch



class Entifier(torch.nn.Module):

	def __init__(self, **config: any):

		super().__init__()

		self.embedding = config.get("embedding", 32)
		self.dimension = config.get("dimension", 128)
		self.number_layers = config.get("number_layers", 2)
		self.dropout = config.get("dropout", 0.1)

		self.tag_to_index = {
			"O": 0, 
			"B-PERSON": 1, "I-PERSON": 2,
			"B-LOCATION": 3, "I-LOCATION": 4, 
			"B-GEOPOLITICAL": 5, "I-GEOPOLITICAL": 6, 
			"B-TIME": 7, "I-TIME": 8,
			"B-ORGANIZATION": 9, "I-ORGANIZATION": 10,
			"B-EVENT": 11, "I-EVENT": 12,
			"B-NATURAL": 13, "I-NATURAL": 14,
			"B-ARTIFACT": 15, "I-ARTIFACT": 16
		}
		self.index_to_tag = { index : tag for tag, index in self.tag_to_index.items() }
		self.tag_padding_index = len(self.tag_to_index)
		self.tag_size = len(self.tag_to_index) + 1

		self.hidden = torch.nn.LSTM(
			input_size = self.embedding,
			hidden_size = self.dimension,
			num_layers = self.number_layers,
			dropout = self.dropout if self.number_layers > 1 else 0.0,
			bidirectional = True,
			batch_first = True
		)
		self.classifier = torch.nn.Linear(self.dimension * 2, self.tag_size)

	def forward(self, embeddings: torch.Tensor) -> torch.Tensor:

		hidden, _ = self.hidden(embeddings)
		logits = self.classifier(hidden)

		return logits

	class Dataset(torch.utils.data.Dataset):

		def __init__(self, texts: list[str], labels: list[str], vectorizer, tag_to_index):

			self.texts = texts
			self.labels = labels

			self.vectorizer = vectorizer

			self.tag_to_index = tag_to_index
			self.index_to_tag = { index : tag for tag, index in tag_to_index.items() }
			self.tag_padding_index = len(tag_to_index)
			self.tag_size = len(tag_to_index) + 1

		def __len__(self):

			return len(self.texts)

		def __getitem__(self, index):

			text = self.texts[index]
			label = self.labels[index]

			return text, label

		def collate(self, batch):

			raw_texts, raw_labels = zip(*batch)

			texts = [" ".join(raw_text) for raw_text in raw_texts]

			with torch.no_grad():
			
				_, _, _, embeddings = self.vectorizer.inference(texts)

			batch_dimension, layer_dimension, _ = embeddings.shape		
			labels = torch.full((batch_dimension, layer_dimension), self.tag_padding_index, dtype = torch.long)

			for i, (raw_text, raw_labels_) in enumerate(zip(raw_texts, raw_labels)):

				labels_ = []

				for token, raw_label in zip(raw_text, raw_labels_):

					subtokens = [self.vectorizer.model.tokenizer.index_to_token[index] for index in self.vectorizer.model.tokenizer.tokenize(token)]

					if raw_label == "O":

						labels_ += [self.tag_to_index.get("O", self.tag_padding_index)]  * len(subtokens)
			
					else:

						category = raw_label[2:]
					
						if raw_label.startswith("B-"):

							labels_ += [self.tag_to_index.get("B-" + category, self.tag_padding_index)]
							labels_ += [self.tag_to_index.get("I-" + category, self.tag_padding_index)] * (len(subtokens) - 1)

						else:

							labels_ += [self.tag_to_index.get("I-" + category, self.tag_padding_index)] * len(subtokens)

					labels_ += [self.tag_to_index.get("O", self.tag_padding_index)]

				labels_ = labels_[:-1]
				length = min(len(labels_), layer_dimension - 1)
				labels[i, 1 : length + 1] = torch.tensor(labels_[:length], dtype = torch.long)

			return embeddings, labels