import glob
import re
import os


dir_name = os.path.dirname(__file__)
regex = re.compile('[^.,;:?!"\'\s]+')
first_line = re.compile('^.*\r?\n')
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
			corpus.append(cache[filename])
		else:
			all_text = open(filename, 'r').read()
			words = regex.findall(all_text)
			title_list = first_line.findall(all_text)
			if len(title_list) > 0:
				title = title_list[0]
			else:
				title = ""
			normalized = []
			for word in words:
				normalized.append(word.lower())
			cache[filename] = {
				'title': title,
				'filename': filename,
				'text': normalized
			}
			corpus.append(cache[filename])
	return corpus
