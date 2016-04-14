#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import codecs

def construct_url():
	fin = open("businesses.txt", 'r')
	types = [u'太仓市', u'西樵', u'更多购物场所', u'博览中心']
	urls = {}
	while 1:
		line = fin.readline()
		if not line:
			break
		url = line.split(" ^ {")[0]
		tmp = line.split(" ^ {")[1] # Get JSON
		tmp = "{"+tmp
		data = json.loads(tmp)
		if not data.has_key("18"):
			continue
		else:
			if data["18"] not in types:
				if urls.has_key(url):
					urls[url] += 1
				else:
					urls[url] = 1
	return urls

def generate_filtered_tmp(urldic):
	

def main():
    urls_dic = construct_url()
    generate_filtered_tmp(urls_dic)

if __name__ == "__main__":
    main()