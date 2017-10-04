#!python3

import text as text_parser
import utils
import xlsxwriter


def tf_idf(corpus):
	documents_list = []
	texts = 0
	for text_data in corpus:
		texts += 1
		tf_idf_dictionary = {}
		print('Progressing text ' + str(texts) + '/' + str(len(corpus)), end='\r')
		computed_tf = utils.tf(text_data['text'])
		for word in computed_tf:
			tf_idf_dictionary[word] = computed_tf[word] * utils.idf(word, corpus)
		documents_list.append({
			'title': text_data['title'],
			'stats': tf_idf_dictionary
		})
	return documents_list


workbook = xlsxwriter.Workbook('tf-idf.xlsx')
print('Computing TF-IDF ranks')
print('\nDone! Writing results...')
text_no = 0
for dictionary in tf_idf(text_parser.get_text_corpus(100)):
	text_no += 1
	worksheet = workbook.add_worksheet(str(text_no))
	worksheet.write(0, 0, dictionary['title'])
	worksheet.write(1, 0, '#')
	worksheet.write(1, 1, 'Rank')
	worksheet.write(1, 2, 'Word')
	row = 2
	sorted_dict = sorted(dictionary['stats'].items(), key=lambda x: (x[1], x[0]), reverse=True)
	for [key, value] in sorted_dict:
		worksheet.write(row, 0, row)
		worksheet.write(row, 1, value)
		worksheet.write(row, 2, key)
		row += 1
workbook.close()
print('\nDone!')
