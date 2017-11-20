import text
import json
import re


symbol_filter = re.compile('[a-z,!.:?;"]', re.IGNORECASE)

print('Reading data...')
categorized = {
	'business': text.get_text_corpus(root_dir='texts/news/business'),
	'entertainment': text.get_text_corpus(root_dir='texts/news/entertainment'),
	'politics': text.get_text_corpus(root_dir='texts/news/politics'),
	'sport': text.get_text_corpus(root_dir='texts/news/sport'),
	'tech': text.get_text_corpus(root_dir='texts/news/tech')
}
symbol_count = {}

print('Processing...')
for [category, articles] in categorized.items():
	symbol_count[category] = {}
	total = 0
	for article in articles:
		for word in article['text']:
			for char in word:
				if not symbol_filter.match(char):
					continue
				total += 1
				if char not in symbol_count[category]:
					symbol_count[category][char] = 1
				else:
					symbol_count[category][char] += 1
	for symbol in symbol_count[category]:
		symbol_count[category][symbol] /= total

print('Writing results...')
with open('symbol_count.json', 'w') as outfile:
	json.dump(symbol_count, outfile, sort_keys=True, indent=4)

print('Done!')
