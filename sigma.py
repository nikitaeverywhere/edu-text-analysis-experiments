#!python3

import text
import math
import xlsxwriter
import re


corpus = text.get_text_corpus(9999999, 'texts/books')

workbook = xlsxwriter.Workbook('sigma.xlsx')

# In a few words, Sigma method depends on the average distance between the same words in a text.
# Thus, the words which are the most equally distributed along all the document will have the
# highest rank.
for txt in corpus:
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
	sorted_words = sorted(words.items(), key=lambda w: w[1]['s'], reverse=True)
	worksheet = workbook.add_worksheet(re.sub('[\[\]:*?/\\\]', '', txt['title'][0:28]))
	worksheet.write(0, 0, txt['title'])
	worksheet.write(1, 0, '#')
	worksheet.write(1, 1, 'Rank')
	worksheet.write(1, 2, 'Word')
	row = 0
	for word, data in sorted_words:
		row += 1
		worksheet.write(row + 1, 0, row)
		worksheet.write(row + 1, 1, data['s'])
		worksheet.write(row + 1, 2, word)

workbook.close()
print('\nDone!')
