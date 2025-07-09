NER_to_index = {
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
index_to_NER = {index: tag for tag, index in NER_to_index.items()}
NER_padding_index = len(NER_to_index)
NER_size = len(NER_to_index) + 1

def map_NER(input):

	return [NER_to_index.get(tag, NER_padding_index) for tag in input]