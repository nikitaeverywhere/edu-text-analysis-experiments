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
	idf_cache[word] = math.log10(len(corpus) / sum([1.0 for i in corpus if word in i]))
	return idf_cache[word]
