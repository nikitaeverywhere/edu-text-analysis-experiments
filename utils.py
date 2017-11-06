#!python3

import collections
import math


idf_cache = {}


def tf(text):
	"""
	:param text: Text array ["this", "is", "example"]
	:return: tf metric
	"""
	tf_text = collections.Counter(text)
	for i in tf_text:
		tf_text[i] = tf_text[i] / len(text)
	return tf_text


def idf(word, corpus):
	"""
	:param word: word like "example"
	:param corpus: text corpus like [["this"], ["is"], ["example"]]
	:return: idf metric
	"""
	if word in idf_cache:
		return idf_cache[word]
	idf_cache[word] = math.log10(len(corpus) / sum([1.0 for i in corpus if word in i['text_set']]))
	return idf_cache[word]


def tf_idf(corpus):
	documents_list = []
	texts = 0
	for text_data in corpus:
		texts += 1
		tf_idf_dictionary = {}
		print('Progressing text ' + str(texts) + '/' + str(len(corpus)), end='\r')
		computed_tf = tf(text_data['text'])
		for word in computed_tf:
			tf_idf_dictionary[word] = computed_tf[word] * idf(word, corpus)
		documents_list.append({
			'title': text_data['title'],
			'stats': tf_idf_dictionary
		})
	return documents_list


def sigma(txt):
	words = {}
	for i, word in enumerate(txt['text']):
		if word in words:
			words[word]['number'] += 1
			words[word]['sum'] += i - words[word]['last_pos']
			words[word]['sum2'] += (i - words[word]['last_pos']) ** 2
			words[word]['last_pos'] = i
		else:
			words[word] = {
				'number': 1,
				'last_pos': i,
				'sum': 0,
				'sum2': 0
			}
	for word, data in words.items():
		s1 = data['sum'] / data['number']
		s2 = data['sum2'] / data['number']
		data['s'] = math.sqrt(math.fabs((s2 ** 2) - (s1 ** 2))) / s1 if s1 != 0 else 1
	return sorted(words.items(), key=lambda w: w[1]['s'], reverse=True)
