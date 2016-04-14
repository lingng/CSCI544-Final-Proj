#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import codecs

fname = "businesses.txt"
fin = open(fname, 'r')
types = [u'太仓市', u'西樵', u'更多购物场所', u'博览中心']
urls = {}
with codecs.open("urls.txt", 'w', encoding="utf-8") as fout:
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
	for url in urls.iterkeys():
		fout.write(url)
		fout.write("\n")

