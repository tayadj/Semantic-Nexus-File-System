


class Tokenizer:

	def __init__(self):

		self.token_to_index = {}
		self.index_to_token = {}

	@property
	def size(self):

		return len(self.token_to_index)

	def fit(self, corpus):

		vocabulary = {token for text in corpus for token in text.split()}

		self.token_to_index = { word : index for index, word in enumerate(vocabulary, start = 1) }
		self.token_to_index["<PADDING>"] = 0

		self.index_to_token = { index : word for index, word in enumerate(vocabulary, start = 1) }
		self.index_to_token[0] = ["<PADDING>"]

		# Implement service token general support