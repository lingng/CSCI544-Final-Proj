#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import codecs
import urllib2

def call_ltp(line):
    url_get_base = "http://api.ltp-cloud.com/analysis/?"
    api_key = 'F6k2x8z9LYEXRx5SHp9WHNhdLpAG9AxuLXknfTld'
    text = line
    format = 'plain'
    pattern = 'ws'
    result = urllib2.urlopen("%sapi_key=%s&text=%s&format=%s&pattern=%s" % (url_get_base,api_key,text,format,pattern))
    content = result.read().strip()
    return content


fname = "input.txt"
# out = "output.txt"

fin = open(fname, 'r')
# with codecs.open(out, 'w', encoding="utf-8") as fout:

while 1:
    line = fin.readline()
    if not line:
        break
    tmp = line.split(" ^ {")[1] # Get JSON
    tmp = "{"+tmp
    # print tmp
    data = json.loads(tmp)
    c = data['content']
    # print c
    # print len(c.split('\n'))
    print call_ltp('里面有一些进口食品还是不错的，但个人感觉商品种类比较少，而且管理不是很灵活，退货比较麻烦。价格方面是比较适中的。')
    # lines = c.split('\n')
    # for i in range(0, len(lines)):
    # 	print call_ltp(lines[i])
