import collections
import json
import re



class Tokenizer:

	def __init__(self, settings):

		self.token_to_index = {}
		self.index_to_token = {}
		self.merges = {}

		self.specials = ["<PADDING>", "<UNKNOWN>", "<CLASS>", "<MASK>"]
		parts = [re.escape(token) for token in self.specials]
		parts += [r"\s+", r"\S+"]
		pattern = "(" + ")|(".join(parts) + ")"
		self.protected = re.compile(pattern)

		self.settings = settings

	def __getattr__(self, name):

		if name == "size":

			return len(self.token_to_index)

		if name == "index_padding":

			return self.token_to_index["<PADDING>"]

		if name == "index_unknown":

			return self.token_to_index["<UNKNOWN>"]

		if name == "index_class":

			return self.token_to_index["<CLASS>"]

		if name == "index_mask":

			return self.token_to_index["<MASK>"]

		raise AttributeError(f"{type(self).__name__!r} has no attribute {name!r}")

	def fit(self, corpus: list[str], size: int = 10000, threshold: int = 10):

		text = " ".join(corpus)

		chars = [chr(index) for index in range(256)]
		chars.extend(char for char in sorted(set(text)) if char not in chars)

		self.index_to_token = { index : token for index, token in enumerate(chars) }
		self.token_to_index = { token : index for index, token in self.index_to_token.items() }

		for token in self.specials:

			if token not in self.token_to_index:

				index = len(self.token_to_index)
				self.token_to_index[token] = index
				self.index_to_token[index] = token

		indices = [self.token_to_index[token] for token in text]

		forbidden_chars = set("!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n\r")
		forbidden_indices = { 
			index 
			for index, token in self.index_to_token.items() 
			if any(char in forbidden_chars for char in token)
		}

		for index in range(len(self.token_to_index), size):

			print(index)

			pairs = collections.Counter(zip(indices, indices[1:]))

			for pair in list(pairs):

				if pair[0] in forbidden_indices or pair[1] in forbidden_indices:

					del pairs[pair]

			if not pairs:

				break

			(pair, frequency) = pairs.most_common(1)[0]

			if frequency < threshold:

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

	def tokenize(self, token: str) -> list[int]:

		indices = [self.token_to_index.get(char, self.token_to_index["<UNKNOWN>"]) for char in token]
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
		
		for match in self.protected.finditer(text):

			token = match.group(0)
			tokens.append(token)

		indices = []

		for token in tokens:

			if token in self.token_to_index:

				indices.append(self.token_to_index[token])

			else:

				indices.extend(self.tokenize(token))

		return indices

	def decode(self, indices: list[int]) -> str:

		text = ""

		for index in indices:

			text += self.index_to_token[index]

		return text

	def load(self):

		with open(self.settings.tokenizer.vocabulary, "r", encoding = "utf-8") as file:

			vocabulary = json.load(file)
			self.index_to_token = { int(index) : token for index, token in vocabulary.items() }
			self.token_to_index = { token : int(index) for index, token in vocabulary.items() }

		with open(self.settings.tokenizer.merges, "r", encoding = "utf-8") as file:

			data = json.load(file)
			bias = data["bias"]

			for offset, pair in enumerate(data["pairs"]):

				self.merges[tuple(pair)] = bias + offset

	def save(self):

		with open(self.settings.tokenizer.vocabulary, "w", encoding = "utf-8") as file:

			json.dump(
				{ index : token for index, token in self.index_to_token.items() },
				file,
				ensure_ascii = False,
				separators = (",", ":")
			)

		with open(self.settings.tokenizer.merges, "w", encoding = "utf-8") as file:

			bias = min(self.merges.values())
			pairs = [list(pair) for pair, index in sorted(self.merges.items(), key = lambda x : x[1])]
			payload = {"bias" : bias, "pairs": pairs}

			json.dump(
				payload, 
				file, 
				ensure_ascii = False, 
				separators = (",", ":")
			)
