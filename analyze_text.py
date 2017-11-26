import text
import utils
import os
import sys
import writer
from slugify import slugify
from nltk import pos_tag


NOUN_THRESHOLD = 0.20

dir_name = os.path.dirname(os.path.realpath(__file__))
file_name = sys.argv[1] if len(sys.argv) > 1 else "texts/news/tech/001.txt"
file_path = os.path.normpath(os.path.join(dir_name, file_name))

if not os.path.isfile(file_path):
	print('File ' + file_path + ' not found')
	exit(1)

print('Reading text corpus...')
corpus = text.get_text_corpus(9999, os.path.normpath('texts/news/tech'))
corpus2 = text.get_text_corpus(9999, os.path.normpath('texts/news/tech'))
print('Analyzing text ' + file_name)

main_text = None
for text in corpus2:
	# print(text['filename'] + '  --  ' + file_path)
	if text['filename'] == file_path:
		main_text = text
if not main_text:
	print('A mystery duck found')
	exit(1)


def parse_text(text_corpus, primary_text):
	print('Tagging text...')
	words = primary_text['text']
	tags = list(map(lambda tagged: tagged[1], pos_tag(words)))  # todo: tag non-normalized form
	tf_idf_line = utils.tf_idf_normalized(text_corpus, primary_text)
	data = [["Word", "Rank", "Tag"]]
	for i in range(0, len(words)):
		data.append([words[i], tf_idf_line[i], tags[i]])
	title = slugify(primary_text["title"])
	directory = os.path.join("analyzed", title)
	print('Writing result to ' + directory)
	writer.write_to_xlsx(os.path.join(directory, title + ".xlsx"), primary_text["title"], data)
	print('Done. Building graph...')
	graph = build_graph(words, tags, tf_idf_line)
	write_graph(graph, directory, title)


def build_graph(words, tags, values):

	node_id = 0
	edges = {}
	nodes = {}

	def is_noun(index):
		return tags[index] == "NN" or tags[index] == "NNS" or tags[index] == "NNP" \
			or tags[index] == "NNPS" or tags[index] == "JJ" or tags[index] == "JJR" \
			or tags[index] == "JJS"

	def is_verb(index):
		return tags[index] == "VB" or tags[index] == "VBZ" or tags[index] == "VBD" \
		    or tags[index] == "VBG" or tags[index] == "VBN"

	def ensure_node(name):
		nonlocal node_id
		if name in nodes:
			return
		nodes[name] = {
			"id": node_id,
			"label": name
		}
		node_id += 1

	def ensure_edge(n1, v, n2):
		edge_uid = str(nodes[n1]["id"]) + "-" + str(nodes[n2]["id"])
		if edge_uid in edges:
			return
		edges[edge_uid] = {
			"source": nodes[n1]["id"],
			"target": nodes[n2]["id"],
			"labels": {v},
			"weight": 1
		}

	def add_edge(n1, v, n2):
		edge_uid = str(nodes[n1]["id"]) + "-" + str(nodes[n2]["id"])
		ensure_edge(n1, v, n2)
		edges[edge_uid]["labels"].add(v)
		edges[edge_uid]["weight"] += 1

	def add_to_graph(n1, v, n2):
		if n1 > n2:
			temp = n1
			n1 = n2
			n2 = temp
		ensure_node(n1)
		ensure_node(n2)
		add_edge(n1, v, n2)

	def expand(index):
		if index + 2 >= len(values):
			return index + 1
		ltb, rtb = index, index
		while ltb > 0 and is_noun(ltb - 1):
			ltb -= 1
		while rtb < len(values) - 1 and is_noun(rtb + 1):
			rtb += 1
		left, right = ltb, rtb
		while left > 0 and is_verb(left - 1):
			left -= 1
		while right < len(values) - 1 and is_verb(right + 1):
			right += 1
		main_noun = " ".join(words[ltb:rtb+1])
		left_verb = " ".join(words[left:ltb]) if left != ltb else None
		right_verb = " ".join(words[rtb+1:right+1]) if right != rtb else None
		ltb = left
		rtb = right
		while left_verb and left > 0 and is_noun(left - 1):
			left -= 1
		while right_verb and right < len(values) - 1 and is_noun(right + 1):
			right += 1
		left_noun = " ".join(words[left:ltb]) if left != ltb else None
		right_noun = " ".join(words[rtb+1:right+1]) if right != rtb else None
		if left_noun:
			add_to_graph(left_noun, left_verb, main_noun)
		if right_noun:
			add_to_graph(right_noun, right_verb, main_noun)
		return right + 1

	i = 0
	while i < len(values):
		if values[i] < NOUN_THRESHOLD or not is_noun(i):
			i += 1
			continue
		i = expand(i)

	return {
		"edges": edges,
		"nodes": nodes
	}


def write_graph(graph, directory, title):
	node_data = [["Id", "Label"]]
	edge_data = [["Source", "Target", "Id", "Label", "Weight"]]
	edge_id = 0
	for node in graph["nodes"].values():
		node_data.append([node["id"], node["label"]])
	for edge in graph["edges"].values():
		for label in edge["labels"]:
			edge_data.append([edge["source"], edge["target"], edge_id, label, edge["weight"]])
			edge_id += 1
	writer.write_to_xlsx(os.path.join(directory, title + "-nodes.xlsx"), title, node_data)
	writer.write_to_xlsx(os.path.join(directory, title + "-edges.xlsx"), title, edge_data)


parse_text(corpus, main_text)
