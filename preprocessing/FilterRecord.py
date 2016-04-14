#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import codecs

"""
	Return a dictionary of urls that are restaurants
"""
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

def get_records_num(urls):
	total_records_num = 0
	fin = open("reviews.txt", 'r')
	while 1:
		line = fin.readline()
		if not line:
			break
		if "flavor\":-1" in line:
			continue
		if "environment\":-1" in line:
			continue
		if "service\":-1" in line:
			continue
		if "content\":\"\"" in line:
			continue
		url = line.split(" ^ {")[0]
		if urls.has_key(url):
			total_records_num += 1
	return total_records_num

def split_files(file_num, urls):
	num_per_file = 3400000 / file_num
	fin = open("reviews.txt", 'r')
	for i in range(0, file_num):
		out = "o_"+str(i)+".txt"
		fout = open(out, 'w')
		count = 0
		while 1:
			if count >= num_per_file:
				break
			line = fin.readline()
			if not line:
				break
			if "flavor\":-1" in line:
				continue
			if "environment\":-1" in line:
				continue
			if "service\":-1" in line:
				continue
			if "content\":\"\"" in line:
				continue
			url = line.split(" ^ {")[0]
			if urls.has_key(url):
				count += 1
				fout.write(line)

def main():
    urls_dic = construct_url()
    # print get_records_num(urls_dic)    #3363141
    split_files(100, urls_dic)

if __name__ == "__main__":
    main()