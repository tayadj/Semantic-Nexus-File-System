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

		self.protected_patterns = [
			("<ELLIPSIS>", re.compile(r"\.{3,}")),
			("<TIME>", re.compile(r"\b\d{1,2}:\d{2}(?::\d{2})?\b")),
			("<MERIDIEM>", re.compile(r"(?<!\w)(?:am|pm|a\.m\.|p\.m\.)(?!\w)", re.IGNORECASE)),
			("<DECIMAL>", re.compile(r"\b\d+\.\d+\b")),
			("<COMMERICAL>", re.compile(r"(?<!\w)(?:ltd|inc|co|corp|llc)\.(?!\w)", re.IGNORECASE)),
			("<INDIAN>", re.compile(r"\b\d{1,3}(?:,\d{2})*(?:,\d{3})\b")),
			("<URL>", re.compile(r"https?://[^\s]+")),
			("<EMAIL>", re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b")),
			("<ABBREVIATION>", re.compile(r"(?<!\w)(?:[A-Za-z]\.){2,}(?!\w)")),
			("<SHORT>", re.compile(r"(?<!\w)(?:(?:jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)|[A-Za-z])\.(?!\w)", re.IGNORECASE)),
			("<TITLE>", re.compile(r"\b(?:mr|mrs|ms|dr|prof|sr|jr|co|st)\.(?!\w)", re.IGNORECASE)),
			("<CONTRACTION>", re.compile(r"(?:n[']t|['](?:s|re|ve|ll|d|m|n))\b", re.IGNORECASE))
		]

	def preprocess(self, text):

		text = text.lower()

		text = re.sub(r"(\w+)(n[']t|['](?:s|re|ve|ll|d|m|n))\b", r"\1 \2", text, flags=re.IGNORECASE)

		placeholders = {}

		for index, (tag, pattern) in enumerate(self.protected_patterns):

			def replace(match):

				key = f"__{tag}{index}__"
				placeholders[key] = match.group(0)

				return key

			text = pattern.sub(replace, text)

		text = re.sub(r'([.,!?;:"(){}\[\]])', r' \1 ', text)
		text = re.sub(r'\s+', ' ', text).strip()

		for key, original in placeholders.items():
		
			text = text.replace(key, original)

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