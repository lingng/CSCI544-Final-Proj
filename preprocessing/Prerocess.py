#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import sys
import codecs
import jieba
from langdetect import detect

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
def replace_punctuation(paragraph):
	punctuation_dic = {
		u'。':u'.',
		u'，':u',',
		u'！':u'!',
		u'：':u':',
		u'（':u'(',
		u'）':u')',
		u'’':u'\'',
		u'；':u';',
		u'、':u',',
		u'～':u'~',
		u'“':u'"',
		u'”':u'"',
		u'＝':u'=',
		u'＊':u'*',
		u'？':u'?'
	}
	for key, value in punctuation_dic.iteritems():
		paragraph = value.join(paragraph.split(key))
	return paragraph

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
	print "====="

def segmentation(content):
	if detect(content) == "zh-cn":
		print content

		# tmp = call_ltp(c)

def preprocess(fname):
	fin = codecs.open(fname, encoding='utf-8')

	while 1:
		line = fin.readline()
		if not line:
		    break
		tmp = line.split(" ^ {")[1] # Get JSON
		tmp = "{"+tmp
		data = json.loads(tmp)
		content = data['content']
		error_correction(content)
		# segmentation(content)
		# print content
		# para = combine_to_one_para(content)
		# para = replace_punctuation(para)

"""
	Main Function
"""
def main(start_idx, end_idx):
	global error_dic
	error_dic = construct_error_dic()
	for i in range(start_idx, end_idx):
		fname = "o_"+str(i)+".txt"
		preprocess(fname)

if __name__ == "__main__":
	print "End index not included!"
	if len(sys.argv) < 3:
		print "Error: Please input the start index of input file and the end index of input file."
		sys.exit()
	main(int(sys.argv[1]), int(sys.argv[2]))