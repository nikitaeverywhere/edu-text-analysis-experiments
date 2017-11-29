#!python3

# This program exports 50 most important terms as an adjacent matrix.

from utils import sigma, tf_idf
from text import get_text_corpus
import csv
import os
from slugify import slugify


file = os.path.join(
	os.path.dirname(os.path.realpath(__file__)), os.path.normpath('texts/news/tech/001.txt')
)
max_words = 30


def get_important_words(corpus, text):
	d = tf_idf(corpus, text)[0]['stats']
	return sorted(d, key=d.get, reverse=True)[:max_words]


def task():
	print('Reading text corpus...')
	text_corpus = get_text_corpus(99999, 'texts/news', add_sentences=True)
	master_text = next((x for x in text_corpus if x['filename'] == file), None)
	if not master_text:
		print('No text in specified text corpus found')
		exit(1)
	print('Working with "' + master_text['title'] + '", max_words=' + str(max_words) + '...')
	with open("matrix-tf-idf-" + slugify(master_text['title']) + ".csv", "w") as f:
		writer = csv.writer(
			f, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator='\n'
		)
		words = get_important_words(text_corpus, master_text)
		matrix = [[""]]
		for word in words:
			matrix[0].append(word)

		for word1 in words:
			row = [word1]
			for word2 in words:
				if word1 == word2:
					row.append(0)
					continue
				count = 0
				for sentence in master_text['by_sentence']:
					if word1 in sentence and word2 in sentence:
						count += 1
				row.append(count)
			matrix.append(row)

		writer.writerows(matrix)


task()
print('Done!')
