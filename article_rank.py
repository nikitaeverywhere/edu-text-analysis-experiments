import sys
import os.path
from text import get_text_corpus
from utils import tf_idf
import xlsxwriter
import re


if len(sys.argv) < 2:
	print('Usage: py article_rank.py texts/news/tech/001.txt')
	exit(0)

dir_name = os.path.dirname(os.path.realpath(__file__))
file_path = os.path.normpath(os.path.join(dir_name, sys.argv[1]))

if not os.path.isfile(file_path):
	print('File ' + file_path + ' not found')
	exit(1)

print('Reading all texts from /texts/news...')
corpus = get_text_corpus(root_dir=os.path.normpath('texts/news'))

main_text = None

for text in corpus:
	if text['filename'] == file_path:
		main_text = text

if not main_text:
	print('A mystery duck found')
	exit(1)

word_ranking = tf_idf(corpus, main_text)[0]
workbook = xlsxwriter.Workbook('article-rank.xlsx')
worksheet = workbook.add_worksheet(re.sub('[\[\]:*?/\\\]', '', main_text['title'][0:28]))
worksheet.write(0, 0, main_text['title'])
worksheet.write(1, 0, '#')
worksheet.write(1, 2, 'Word')
worksheet.write(1, 1, 'Rank')
row = 2
for word in main_text['text']:
	worksheet.write(row, 0, row - 1)
	worksheet.write(row, 1, word)
	worksheet.write(row, 2, word_ranking['stats'][word] / word_ranking['max_rank'])
	row += 1
workbook.close()
print('\nDone! Check article-rank.xlsx file.')
