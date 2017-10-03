import glob
import re
import os


dir_name = os.path.dirname(__file__)
regex = re.compile('[^.,;:?!"\'\s]+')
cache = {}


def get_text_corpus(maxfiles=9223372036854775807, root_dir='texts'):
	pattern = os.path.join(root_dir, '**\*.*')
	corpus = []
	files = 0
	for filename in glob.iglob(os.path.join(dir_name, pattern), recursive=True):
		files += 1
		if files > maxfiles:
			break
		if filename in cache:
			words = cache[filename]
		else:
			words = regex.findall(open(filename, 'r').read())
			cache[filename] = words
		normalized = []
		for word in words:
			normalized.append(word.lower())
		corpus.append(normalized)
	return corpus
