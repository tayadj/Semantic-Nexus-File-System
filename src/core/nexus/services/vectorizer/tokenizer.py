import re



class Tokenizer:

	def __init__(self):

		self.token_padding = "<PADDING>"
		self.token_unknown = "<UNKNOWN>"
		self.index_padding = None
		self.index_unknown = None
		self.size = None

		self.token_to_index = {}
		self.index_to_token = {}

	def preprocess(self, text):

		text = text.lower()
		text = re.sub(r'([.,!?;:"(){}\[\]])', r' \1 ', text)
		text = re.sub(r'\s+', ' ', text).strip()

		return text

	def tokenize(self, text):

		text = self.preprocess(text)

		return text.split()

	def fit(self, corpus):

		vocabulary = { token for text in corpus for token in self.tokenize(text) }

		self.token_to_index = { word : index for index, word in enumerate(vocabulary, start = 2) }
		self.token_to_index[self.token_padding] = 0
		self.token_to_index[self.token_unknown] = 1

		self.index_to_token = { index : word for index, word in enumerate(vocabulary, start = 2) }
		self.index_to_token[0] = self.token_padding
		self.index_to_token[1] = self.token_unknown

		self.size = len(self.token_to_index)
		self.index_padding = 0
		self.index_unknown = 1

	def encode(self, text):

		tokens = self.tokenize(text)
		indices = [ self.token_to_index.get(token, self.index_unknown) for token in tokens ]

		return indices