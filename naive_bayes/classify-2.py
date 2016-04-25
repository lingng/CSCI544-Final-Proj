#! /usr/bin/env python
# -*- coding: utf-8 -*-

import pickle
import json
import sys
import copy

_class_num = 2

priors = {
    "service": [0] * _class_num,
    "environment": [0] * _class_num,
    "flavor": [0] * _class_num
}
posteriors = {
    "service": {},
    "environment": {},
    "flavor": {}
}


def classify(w, aspect):
    global priors, posteriors, _class_num
    score = copy.deepcopy(priors[aspect])
    print score,
    print "|"
    for t in w:
        if t in posteriors[aspect]:
            for c in range(_class_num):
                score[c] += posteriors[aspect][t][c]
                print score,
                print "|",
        else:
            pass
            # print "no %s\n" % t
    print "\n"
    max_c = score.index(max(score))   # argmax
    return max_c


def main():
    global priors, posteriors, _class_num
    with open(sys.argv[2], "r") as f:
        priors = pickle.load(f)
        posteriors = pickle.load(f)
        _class_num = pickle.load(f)
        feature = pickle.load(f)
    pathname = sys.argv[1]
    with open(pathname, "r") as f:
        correct_num = 0
        total_num = 0
        for line in f:
            data = json.loads(line, encoding='utf-8')

            if feature == 0:
                words = data["segmentation"].split("/")
            elif feature == 1:
                words = data["pinyin"].split("/")

            test_aspect = "flavor"

            max_c = classify(words, test_aspect)
            if _class_num == 2:
                if data[test_aspect] > 2:
                    ref_rate = 1
                elif data[test_aspect] < 2:
                    ref_rate = 0
                else:
                    continue
            else:
                ref_rate = data[test_aspect]
            print max_c, ref_rate

            if max_c == ref_rate:
                correct_num += 1
                # print correct_num
            total_num += 1
        print correct_num / float(total_num)

if __name__ == "__main__":
    main()
