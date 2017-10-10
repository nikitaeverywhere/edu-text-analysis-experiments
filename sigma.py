#!python3

import text
import xlsxwriter
import re
from utils import sigma


# In a few words, Sigma method depends on the average distance between the same words in a text.
# Thus, the words which are the most equally distributed along all the document will have the
# highest rank.
corpus = text.get_text_corpus(9999999, 'texts/books')
workbook = xlsxwriter.Workbook('sigma.xlsx')
for txt in corpus:
	sorted_words = sigma(txt)
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
