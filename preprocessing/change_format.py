#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import re
import jieba
import codecs
# from xpinyin import Pinyin
import pinyin

# seg_list = jieba.cut("我来到北京清华大学", cut_all=False)
# print("Default Mode: " + "/ ".join(seg_list))  # 精确模式

# p = Pinyin()
# print p.get_pinyin(u"上海", ' ')
# print pinyin.get('你好', format="numerical")

# for i in range(0, 100):
#     fname = "o_"+str(i)+".txt"
#     out = "f_"+str(i)+".txt"

fname = "o_1.txt"
out = "f_1.txt"

fin = open(fname, 'r')
with codecs.open(out, 'w', encoding="utf-8") as fout:

    while 1:
        line = fin.readline()
        if not line:
            break

        # Use " ^ {" to split and get JSON.
        tmp = line.split(" ^ {")[1] # Get JSON
        tmp = "{"+tmp
        # print tmp
        data = json.loads(tmp)

        seg_list = jieba.cut(data['content'], cut_all=False)
        seg = "/".join(seg_list)
        wordlist = jieba.lcut(data['content'], cut_all=False)
        print wordlist
        pylst = []
        for word in wordlist:
            py = pinyin.get(word, format="numerical")
            pylst.append(py)
        # print pylst
        py = "/".join(pylst)
        print py
        # py = pinyin.get(data['content'], format="numerical")
        # print py

        obj = {}
        obj['flavor'] = data['flavor']
        obj['environment'] = data['environment']
        obj['service'] = data['service']
        obj['content'] = data['content']
        obj['segmentation'] = seg
        obj['pinyin'] = py
        print json.dumps(obj,ensure_ascii=False)
        tmpstr = json.dumps(obj,ensure_ascii=False)
        fout.write(tmpstr)
        fout.write('\n')


    #fout.write(line)