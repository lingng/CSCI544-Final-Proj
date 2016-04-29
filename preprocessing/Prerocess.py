#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import sys, os
import codecs
from langdetect import detect
import pinyin
from pyltp import Segmentor


"""
	Eliminate newlines in the comment to use ltp cloud in the future.

	@lines: Comment content (multiple lines)
	return: Comment content (single line)
"""
def combine_to_one_para(lines):
	return ''.join(lines.split("\n"))

"""
	Replace chinese punctuations with english punctuations to work for deep learn algorithm

	@paragraph: Comment content with chinese punctuations
	return: Comment content with english punctuations
"""

def construct_error_dic():
	fin = codecs.open('dic_wrong.txt', encoding='utf-8')
	wrong_dic = {}
	while 1:
		line = fin.readline()
		if not line:
			break
		line = line.strip()
		wrong = line.split("\t")[0]
		correct = line.split("\t")[1]
		wrong_dic[wrong] = correct
	return wrong_dic

def error_correction(content):
	tmp_content = content
	for key, value in error_dic.iteritems():
		if tmp_content.find(key) != -1:
			tmp_content = value.join(tmp_content.split(key))
	if tmp_content != content:
		print content
		print tmp_content

"""
	Use ltp API for segmentation

	@line: input line
"""
def call_ltp(line):
	line =  ''.join(line.encode("utf-8").splitlines())
	url_get_base = "http://api.ltp-cloud.com/analysis/?"
	api_key = 'F6k2x8z9LYEXRx5SHp9WHNhdLpAG9AxuLXknfTld'
	text = line
	format = 'plain'
	pattern = 'ws'

	obj = {'api_key': api_key, 'text': text, 'format': format, 'pattern': pattern}
	r = requests.get(url_get_base, params=obj)
	content = r.content
	return content

"""
	Combine segmetation results. Use '/' to separate different words

	@contents: Segmentation results
	return: use '/' to separate different words instead of "\\n" and spaces
"""
def combine_segmentation_result(contents):
	rst = '/'.join(contents.split("\n"))
	rst = '/'.join(rst.split(" "))
	return rst

"""
	Add PinYin for segmentations

	@segmentation: Segmentation for the input
	return: Use '/' to separate the pinyin for different words
"""
def add_pinyin(segmentation):
	pylst = []
	for word in segmentation.split('/'):
		py = pinyin.get(word, format="numerical")
		pylst.append(py)
	return '/'.join(pylst)

"""
	Use pyltp for segmentation

	@index: index of the input file.
"""
def process(index):

	ROOTDIR = os.path.join(os.path.dirname(__file__), os.pardir)
	sys.path.append(os.path.join(ROOTDIR, "lib"))

	# Set your own model path
	MODELDIR=os.path.join(ROOTDIR, "ltp_data")

	segmentor = Segmentor()
	segmentor.load(os.path.join(MODELDIR, "cws.model"))

	finname = "o_"+str(index)+".txt"
	foutname = "p_"+str(index)+".txt"
	print finname
	count = 0
	fin = codecs.open(finname, encoding='utf-8')
	with codecs.open(foutname, 'w', encoding="utf-8") as fout:
		while 1:
			line = fin.readline()
			if not line:
			    break
			tmp = line.split(" ^ {")[1] # Get JSON
			tmp = "{"+tmp
			data = json.loads(tmp)
			content = data['content']
			# error_correction(content)
			content = content.strip()
			segmentation = ""
			for line in content.split("\n"):
				line = line.encode("utf-8")
				words = segmentor.segment(line)
				segmentation += "/".join(words)
				segmentation += "/"

			# Return type of the function is str, not unicode. Thus need to change into unicode.
			segmentation = unicode(segmentation, "utf-8")
			pinyin = add_pinyin(segmentation)
			obj = {}
			obj['flavor'] = data['flavor']
			obj['environment'] = data['environment']
			obj['service'] = data['service']
			obj['content'] = data['content']
			obj['segmentation'] = segmentation
			obj['pinyin'] = pinyin
			tmpstr = json.dumps(obj,ensure_ascii=False)
			fout.write(tmpstr)
			fout.write('\n')
			count += 1
			print count
		segmentor.release()

def preprocess(index):
	finname = "o_"+str(index)+".txt"
	foutname = "f_"+str(index)+".txt"
	fin = codecs.open(finname, encoding='utf-8')
	with codecs.open(foutname, 'w', encoding="utf-8") as fout:
		while 1:
			line = fin.readline()
			if not line:
			    break
			tmp = line.split(" ^ {")[1] # Get JSON
			tmp = "{"+tmp
			data = json.loads(tmp)
			content = data['content']
			# error_correction(content)
			content = content.strip()
			rst = ""
			for item in content.split("\n"):
				rst += call_ltp(item)
				rst += "\n"
			
			segmentation = combine_segmentation_result(rst)
			# Return type of the function is str, not unicode. Thus need to change into unicode.
			segmentation = unicode(segmentation, "utf-8")
			pinyin = add_pinyin(segmentation)
			obj = {}
			obj['flavor'] = data['flavor']
			obj['environment'] = data['environment']
			obj['service'] = data['service']
			obj['content'] = data['content']
			obj['segmentation'] = segmentation
			obj['pinyin'] = pinyin
			print segmentation
			tmpstr = json.dumps(obj,ensure_ascii=False)
			fout.write(tmpstr)
			fout.write('\n')
			
"""
	Main Function
"""
def main(start_idx, end_idx):
	for i in range(start_idx, end_idx):
		fname = "o_"+str(i)+".txt"
		process(i)

if __name__ == "__main__":
	print "End index not included!"
	if len(sys.argv) < 3:
		print "Error: Please input the start index of input file and the end index of input file."
		sys.exit()
	main(int(sys.argv[1]), int(sys.argv[2]))