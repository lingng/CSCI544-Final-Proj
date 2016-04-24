#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import codecs
from langdetect import detect

"""
	Return a dictionary of urls that are restaurants

	return: dictionary of urls. Key: url; Value: Number of times the url appears
"""
def construct_url():
	fin = open("businesses.txt", 'r')
	line = fin.readline()
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

"""
	Get the records number

	@urls: The dictionary of urls for restaurants.
	return: total records number that meets the requirement of our project
"""
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
		tmp = line.split(" ^ {")[1] # Get JSON
		tmp = "{"+tmp
		data = json.loads(tmp)
		content = data['content']
		content = content.strip()
		if urls.has_key(url):
			try:
				if detect(content) == "zh-cn":
					total_records_num += 1
					print total_records_num
			except:
				continue			
	return total_records_num

"""
	Split files into given number of subfiles.
	Output file name format: o_[index].txt

	@file_num: Given number for how many subfiles we need
	@urls: Dictionary of restaurants urls.
"""
def split_files(file_num, urls):
	num_per_file = 3400000 / 200
	fin = codecs.open("reviews.txt", encoding='utf-8')
	line = fin.readline()
	for i in range(0, file_num):
		out = "o_"+str(i)+".txt"
		print out
		with codecs.open(out, 'w', encoding="utf-8") as fout:
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
				tmp = line.split(" ^ {")[1] # Get JSON
				tmp = "{"+tmp
				data = json.loads(tmp)
				content = data['content']
				content = content.strip()
				if urls.has_key(url):
					try:
						if detect(content) == "zh-cn":
							count += 1
							print count
							fout.write(line)
					except:
						continue

"""
	Main Function
"""
def main():
    urls_dic = construct_url()
    split_files(190, urls_dic)


if __name__ == "__main__":
    main()