# Classify text by its spectre

import os
import sys
import re
import glob
import json


spectre_file = 'symbol_count.json'
base_dir = os.path.normpath('texts/news/')
file_name = os.path.normpath(os.path.join(
	base_dir, sys.argv[1] if len(sys.argv) > 1 else 'tech/001.txt'
))
symbol_filter = re.compile('[a-z]', re.IGNORECASE)
first_line = re.compile('^.*\r?\n')

# if not os.path.exists(file_name):
# 	print('No article found ' + file_name)
# 	exit(1)
if not os.path.exists(spectre_file):
	print('No spectre file ' + spectre_file + ', launch letters_count.py first!')
	exit(1)

classified = json.loads(open(spectre_file, 'r').read())


def classify_text(f_name, output=True):
	text_chars = {}
	all_chars = 0
	text = open(f_name, 'r').read()
	possible_title = first_line.findall(text)
	if len(possible_title) > 0:
		text_title = possible_title[0].strip()
	else:
		text_title = ""
	for char in text:
		if not symbol_filter.match(char):
			continue
		char = char.lower()
		all_chars += 1
		if char not in text_chars:
			text_chars[char] = 1
		else:
			text_chars[char] += 1

	if output:
		print('Article "' + text_title + '" classification score:')
	min_correlation = sys.maxsize
	classified_as = 'duck'
	all_cats = {}
	for category in classified:
		correlation = 0
		for char in classified[category]:
			classified_score = classified[category][char]
			text_score = text_chars[char] / all_chars if char in text_chars else 0
			correlation += abs(classified_score - text_score)
		if correlation < min_correlation:
			min_correlation = correlation
			classified_as = category
		all_cats[category] = correlation

	sorted_dict = sorted(all_cats.items(), key=lambda x: (x[1], x[0]), reverse=False)
	guesses = []
	for [cat, value] in sorted_dict:
		guesses.append(cat)
		if output:
			print(cat + ': ' + str(value))

	if output:
		print('Article is most likely about ' + classified_as + '!')

	return guesses


files = []
for file in glob.iglob(file_name, recursive=True):
	files.append(file)

if len(files) == 0:
	print('Cannot find any file matching ' + file_name + '; try specifying "tech/*" parameter')
	exit(1)

# If single file, classify it
if len(files) == 1:
	classify_text(files[0], output=True)
	exit(0)

# If multiple files, see stats of classification
cat_stats = {}
for file in files:
	categories = classify_text(file, output=False)
	if categories[0] not in cat_stats:
		cat_stats[categories[0]] = 1
	else:
		cat_stats[categories[0]] += 1
print('In ' + str(len(files)) + ' files the next categories were classified:')
for [c, n] in sorted(cat_stats.items(), key=lambda x: (x[1], x[0]), reverse=True):
	print(c + ' for ' + str(n) + ' files')
