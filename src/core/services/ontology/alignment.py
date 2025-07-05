import re



def ontology_alignment(text):

	"""
	text = text.lower()
	
	mapping = {
		r'\bartificial intelligence\b': "Artificial Intelligence",
		r'\bai\b': "Artificial Intelligence",

		r'\bmachine learning\b': "Machine Learning",
		r'\bml\b': "Machine Learning",
		r'\bdeep learning\b': "Deep Learning",
		r'\bneural network(?:s)?\b': "Neural Networks",
		r'\brnn\b': "Recurrent Neural Networks",
		r'\bcnn\b': "Convolutional Neural Networks",
		r'\bgan\b': "Generative Adversarial Networks",

		r'\bnatural language processing\b': "Natural Language Processing",
		r'\bnlp\b': "Natural Language Processing",

		r'\bcomputer vision\b': "Computer Vision",
		r'\bcv\b': "Computer Vision",

		r'\bdata science\b': "Data Science",
		r'\bbig data\b': "Big Data",
		r'\bdata analytics\b': "Data Analytics",

		r'\brobotics\b': "Robotics",
		r'\binternet of things\b': "Internet of Things",
		r'\biot\b': "Internet of Things",

		r'\bpython( language)?\b': "Python",
		r'\bjs\b': "JavaScript",
		r'\bjavascript\b': "JavaScript",
		r'\bnode\.?js\b': "Node.js",

		r'\bos\b': "Operating System",
		r'\bdatabase(?:s)?\b': "Database",
	}
	
	for pattern, canonical in mapping.items():

		text = re.sub(pattern, canonical, text, flags = re.IGNORECASE)
	
	for canonical in set(mapping.values()):

		duplication_pattern = re.compile(re.escape(canonical) + r'\s*\(\s*' + re.escape(canonical) + r'\s*\)', flags = re.IGNORECASE)
		text = duplication_pattern.sub(canonical, text)
	
	text = re.sub(r'\s+', ' ', text).strip()
	"""

	return text