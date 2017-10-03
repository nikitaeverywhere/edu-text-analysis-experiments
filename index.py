#!python3

import text
import utils


def tf_idf(corpus):
	documents_list = []
	texts = 0
	for strings in corpus:
		texts += 1
		tf_idf_dictionary = {}
		print('Progressing text ' + str(texts) + '/' + str(len(corpus)), end='\r')
		computed_tf = utils.tf(strings)
		for word in computed_tf:
			tf_idf_dictionary[word] = computed_tf[word] * utils.idf(word, corpus)
		documents_list.append(tf_idf_dictionary)
	return documents_list


# Todo: write the result to excel sheets
print('Computing TF-IDF ranks')
tf_idf(text.get_text_corpus(10))
print('\nDone!')
