#!python3

# This program exports 50 most important terms as an adjacent matrix.

from utils import sigma
from text import get_text_corpus
import csv


def get_important_words(corpus):
	words = []
	i = 0
	for word, data in sigma(corpus):
		i += 1
		if i > 100:
			break
		words.append(word)
	return words


def task():
	with open("gephi.csv", "w") as f:
		writer = csv.writer(
			f, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator='\n'
		)
		text = get_text_corpus(1, 'texts/books', add_sentences=True)[0]
		words = get_important_words(text)
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
				for sentence in text['by_sentence']:
					if word1 in sentence and word2 in sentence:
						count += 1
				row.append(count)
			matrix.append(row)

		writer.writerows(matrix)


task()
print('Done!')
