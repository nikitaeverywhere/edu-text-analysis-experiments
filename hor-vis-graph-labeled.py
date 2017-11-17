import utils
import text as text_parser
import os
from slugify import slugify
from nltk import word_tokenize, pos_tag
import xlsxwriter


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
	tags = pos_tag(text)  # 'VB', 'VBP'
	commons = set()
	for word in text:
		rank = ranks[word] / max_rank
		line.append(rank)
		if rank < rank_threshold:
			commons.add(word)

	hvg = {}
	all_words = set(text) - commons
	used_words = set()

	def add_to_hvg(w1, w2, label=None):
		if w1 > w2:
			temp = w1
			w1 = w2
			w2 = temp
		if w1 not in hvg:
			hvg[w1] = {}
		used_words.add(w1)
		used_words.add(w2)
		if label:
			if w2 not in hvg[w1]:
				hvg[w1][w2] = [1, label]
			else:
				hvg[w1][w2][1] = label
			return
		if w2 not in hvg[w1]:
			hvg[w1][w2] = [0, '']
		hvg[w1][w2][0] += 1

	limit = len(line)
	for current in range(0, limit):
		if line[current] < rank_threshold:
			continue
		label = None
		labelScore = 0
		for left in reversed(range(max(0, current - horizon), max(0, current - 1))):
			if line[left] > line[current]:
				add_to_hvg(text[left], text[current], label)
				break
			else:
				if (tags[left][1] == 'VB' or tags[left][1] == 'VBP') and line[left] > labelScore:
					labelScore = line[left]
					label = tags[left][0]
		label = None
		labelScore = 0
		for right in range(min(limit, current + 1), min(limit, current + horizon)):
			if line[right] > line[current]:
				add_to_hvg(text[right], text[current], label)
				break
			else:
				if (tags[right][1] == 'VB' or tags[right][1] == 'VBP') and line[right] > labelScore:
					labelScore = line[right]
					label = tags[right][0]

	if not os.path.isdir('hor-vis-graph'):
		os.mkdir('hor-vis-graph')
	# with open("hor-vis-graph/" + slugify(all_texts[i]['title']) + ".csv", "w") as f:
	# 	writer = csv.writer(
	# 		f, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator='\n'
	# 	)
	# 	matrix = [[""]]
	# 	for word in all_words:
	# 		matrix[0].append(word)
	#
	# 	for word1 in all_words:
	# 		row = [word1]
	# 		for word2 in all_words:
	# 			if word1 > word2:
	# 				wo1 = word2
	# 				wo2 = word1
	# 			else:
	# 				wo1 = word1
	# 				wo2 = word2
	# 			row.append(hvg[wo1][wo2] if wo1 in hvg and wo2 in hvg[wo1] else 0)
	# 		matrix.append(row)
	#
	# 	writer.writerows(matrix)

	title = slugify(all_texts[i]['title'])
	workbookNodes = xlsxwriter.Workbook('hor-vis-graph/' + title + '-nodes.xlsx')
	worksheetNodes = workbookNodes.add_worksheet(title[:28])
	workbookEdges = xlsxwriter.Workbook('hor-vis-graph/' + title + '-edges.xlsx')
	worksheetEdges = workbookEdges.add_worksheet(title[:28])
	worksheetNodes.write(0, 0, 'Id')
	worksheetNodes.write(0, 1, 'Label')
	worksheetEdges.write(0, 0, 'Source')
	worksheetEdges.write(0, 1, 'Target')
	worksheetEdges.write(0, 2, 'Type')
	worksheetEdges.write(0, 3, 'Id')
	worksheetEdges.write(0, 4, 'Label')
	worksheetEdges.write(0, 5, 'Weight')

	words_map = {}
	word_num = 0
	for word in used_words:
		words_map[word] = word_num
		worksheetNodes.write(word_num + 1, 0, word_num)
		worksheetNodes.write(word_num + 1, 1, word)
		word_num += 1
	workbookNodes.close()

	word_num = 0
	for word1 in hvg:
		for word2 in hvg[word1]:
			worksheetEdges.write(word_num + 1, 0, words_map[word1])
			worksheetEdges.write(word_num + 1, 1, words_map[word2])
			worksheetEdges.write(word_num + 1, 2, 'Undirected')
			worksheetEdges.write(word_num + 1, 3, word_num)
			worksheetEdges.write(word_num + 1, 4, hvg[word1][word2][1])
			worksheetEdges.write(word_num + 1, 5, hvg[word1][word2][0])
			word_num += 1
	workbookEdges.close()

print('\nDone!')
