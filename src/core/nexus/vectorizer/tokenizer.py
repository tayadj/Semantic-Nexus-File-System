import collections



class Tokenizer:

	def __init__(self):

		self.token_to_index = {}
		self.index_to_token = {}
		self.merges = {}

	def fit(self, corpus: list[str], size: int = 10000, specials: set[str] = {}):

		text = " ".join(corpus)

		chars = [chr(index) for index in range(256)]
		chars.extend(char for char in sorted(set(text)) if char not in chars)

		self.index_to_token = { index : token for index, token in enumerate(chars) }
		self.token_to_index = { token : index for index, token in self.index_to_token.items() }

		for token in specials:

			if token not in self.index_to_token:

				index = len(self.token_to_index)
				self.token_to_index[token] = index
				self.index_to_token[index] = token

		indices = [self.token_to_index[token] for token in text]

		for index in range(len(self.token_to_index), size):

			if len(indices) == 1:

				break

			pairs = collections.Counter(zip(indices, indices[1:]))
			pair = max(pairs.items(), key = lambda x : x[1])[0]

			if pair is None:

				break

			storage = collections.deque(indices)
			indices = []

			while storage:

				current = storage.popleft()

				if storage and (current, storage[0]) == pair:

					indices.append(index)
					storage.popleft()

				else:

					indices.append(current)

			self.merges[pair] = index
			
		for (left, right), index in self.merges.items():

			merged = self.index_to_token[left] + self.index_to_token[right]
			self.index_to_token[index] = merged
			self.token_to_index[merged] = index

	def preprocess(self, text: str) -> str:

		text = text.replace("\n", " \n ")

		return text

	def tokenize(self, token: str) -> list[int]:

		indices = [self.token_to_index[char] for char in token]
		flag = True
		
		while flag and len(indices) > 1:

			flag = False
			new_indices = []
			position = 0
			
			while position < len(indices) - 1:

				pair = (indices[position], indices[position + 1])

				if pair in self.merges:

					new_indices.append(self.merges[pair])
					flag = True
					position += 2

				else:

					new_indices.append(indices[position])
					position += 1

			if position < len(indices):

				new_indices.append(indices[position])

			indices = new_indices

		return indices


	def encode(self, text: str) -> list[int]:

		tokens = []

		text = self.preprocess(text)
		text = text.split()

		for position, word in enumerate(text):

			if position > 0 and not word.startswith("\n"):

				tokens.append(" " + word)

			else:

				tokens.append(word)

		indices = []

		for token in tokens:

			if token in self.token_to_index:

				indices.append(self.token_to_index[token])

			else:

				subindices = self.tokenize(token)
				indices.extend(subindices)

		return indices

	def decode(self, indices: list[int]) -> str:

		text = ""

		for index in indices:

			token = self.index_to_token[index]

			if token.startswith(" "):

				text += " " + token[1:]

			else:

				text += token

		return text


