#! /usr/bin/env python
# -*- coding: utf-8 -*-

import pickle
import json
import sys

priors = {
    "service": [0] * 5,
    "environment": [0] * 5,
    "flavor": [0] * 5
}
posteriors = {
    "service": {},
    "environment": {},
    "flavor": {}
}


def classify(w, aspect):
    global priors, posteriors
    score = priors[aspect]
    for t in w:
        if t in posteriors[aspect]:
            for c in range(5):
                score[c] += posteriors[aspect][t][c]
        else:
            print "no %s\n" % t
    print score
    max_c = score.index(max(score))   # argmax
    return max_c


def main():
    global priors, posteriors
    with open("nbmodel.txt", "r") as f:
        priors = pickle.load(f)
        posteriors = pickle.load(f)
    pathname = sys.argv[1]
    with open(pathname, "r") as f:
        correct_num = 0
        total_num = 0
        for line in f:
            data = json.loads(line, encoding='utf-8')
            words = data["segmentation"].split("/")
            max_c = classify(words, "environment")
            print max_c, data["environment"]
            if max_c == data["environment"]:
                correct_num += 1
                # print correct_num
            total_num += 1
        print correct_num / float(total_num)

if __name__ == "__main__":
    main()
