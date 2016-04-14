#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import codecs
import urllib2
from langdetect import detect

def call_ltp(line):
	print "---------"
	print line
	line =  ''.join(line.encode("utf-8").splitlines())
	url_get_base = "http://api.ltp-cloud.com/analysis/?"
	api_key = 'F6k2x8z9LYEXRx5SHp9WHNhdLpAG9AxuLXknfTld'
	text = line
	format = 'plain'
	pattern = 'ws'
	result = urllib2.urlopen("%sapi_key=%s&text=%s&format=%s&pattern=%s" % (url_get_base,api_key,text,format,pattern))
	content = result.read().strip()
	return content

def combine_to_one_para(lines):
	print lines
	return ''.join(lines.split("\n"))

fname = "input.txt"
# fname = "o_0.txt"
# out = "output.txt"

fin = open(fname, 'r')

while 1:
	line = fin.readline()
	if not line:
	    break
	tmp = line.split(" ^ {")[1] # Get JSON
	tmp = "{"+tmp
	# print tmp
	data = json.loads(tmp)
	c = data['content']
	t = combine_to_one_para(c)
	print t
	# print call_ltp(t)
	# print c
	# print "---"
	# print c.strip()
	# if detect(c) == "zh-cn":
	# 	print c
		# tmp = call_ltp(c)