import utils
import text as text_parser
import csv
import os
from slugify import slugify
import math


print('Reading texts...')
all_texts = text_parser.get_text_corpus(9999, 'texts/news')
print('Done! Computing TF-IDF ranks...')
all_ranks = utils.tf_idf(all_texts)
print('\nDone! Computing horizontal visibility graph...')

horizon = 20              # do not search in HVG behind the horizon
rank_threshold = 0.01     # filter less relevant words, ranked in range 0..1

for i in range(0, len(all_texts)):

	print(
		'Writing HVG #' + str(i + 1) + '/' + str(len(all_texts))
		+ ' (' + all_texts[i]['title'][:10] + '...)'
		, end='\r'
	)

	line = []
	ranks = all_ranks[i]['stats']
	max_rank = all_ranks[i]['max_rank']
	text = all_texts[i]['text']
	commons = set()
	for word in text:
		rank = ranks[word] / max_rank
		line.append(rank)
		if rank < rank_threshold:
			commons.add(word)

	hvg = {}
	all_words = set(text) - commons

	def add_to_hvg(w1, w2):
		if w1 > w2:
			temp = w1
			w1 = w2
			w2 = temp
		if w1 not in hvg:
			hvg[w1] = {}
		hvg[w1][w2] = 0 if w2 not in hvg[w1] else hvg[w1][w2] + 1

	limit = len(line)
	for current in range(0, limit):
		if line[current] < rank_threshold:
			continue
		for left in reversed(range(max(0, current - horizon), max(0, current - 1))):
			if line[left] > line[current]:
				add_to_hvg(text[left], text[current])
				break
		for right in range(min(limit, current + 1), min(limit, current + horizon)):
			if line[right] > line[current]:
				add_to_hvg(text[right], text[current])
				break

	if not os.path.isdir('hor-vis-graph'):
		os.mkdir('hor-vis-graph')
	with open("hor-vis-graph/" + slugify(all_texts[i]['title']) + ".csv", "w") as f:
		writer = csv.writer(
			f, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator='\n'
		)
		matrix = [[""]]
		for word in all_words:
			matrix[0].append(word)

		for word1 in all_words:
			row = [word1]
			for word2 in all_words:
				if word1 > word2:
					wo1 = word2
					wo2 = word1
				else:
					wo1 = word1
					wo2 = word2
				row.append(hvg[wo1][wo2] if wo1 in hvg and wo2 in hvg[wo1] else 0)
			matrix.append(row)

		writer.writerows(matrix)

print('\nDone!')
