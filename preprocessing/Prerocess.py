#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
import sys
import codecs
# import jieba
import urllib2
from langdetect import detect
import pinyin


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
	# url = r.url
	# result = urllib2.urlopen("%sapi_key=%s&text=%s&format=%s&pattern=%s" % (url_get_base,api_key,text,format,pattern))
	# result = urllib2.urlopen("%s%s" % (url_get_base,parameter))
	# result = urllib2.urlopen(url)
	# content = result.read().strip()
	return content
	# return " "

def combine_segmentation_result(contents):
	print contents
	rst = '/'.join(contents.split("\n"))
	rst = '/'.join(rst.split(" "))
	return rst

def add_pinyin(segmentation):
	pylst = []
	for word in segmentation.split('/'):
		py = pinyin.get(word, format="numerical")
		pylst.append(py)
	return '/'.join(pylst)

def preprocess(fname):
	fin = codecs.open(fname, encoding='utf-8')
	with codecs.open("output.txt", 'w', encoding="utf-8") as fout:
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
			if detect(content) == "zh-cn":
				rst = ""
				for item in content.split("\n"):
					rst += call_ltp(item)
					rst += "\n"
				
				segmentation = combine_segmentation_result(rst)
				# Return type of the function is str, not unicode. Thus need to change into unicode.
				segmentation = unicode(segmentation, "utf-8")
				pinyin = add_pinyin(segmentation)
				# print pinyin
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
	        
			
		# print content
		# para = combine_to_one_para(content)
		# para = replace_punctuation(para)

"""
	Main Function
"""
def main(start_idx, end_idx):
	# global error_dic
	# error_dic = construct_error_dic()
	preprocess("input.txt")
	# for i in range(start_idx, end_idx):
	# 	fname = "o_"+str(i)+".txt"
	# 	preprocess(fname)

if __name__ == "__main__":
	print "End index not included!"
	if len(sys.argv) < 3:
		print "Error: Please input the start index of input file and the end index of input file."
		sys.exit()
	main(int(sys.argv[1]), int(sys.argv[2]))