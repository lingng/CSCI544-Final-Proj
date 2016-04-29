#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys

import math
import json
try:
    import cPickle as pickle
except:
    import pickle
import glob

feature = None  # 0 phrases only, 1 pinyin only, 2 mixed
n_gram = None
aspect = None

voc = dict()

c = 0

priors = [0, 0]
posteriors = {}


def learn_one(data, words):
    """ train model of specific aspect.

    args:
        aspect: belongs to one of {"service", "environment", "flavor"}
        data: json format, containing information of one review
              {
                content:
                segmentation:
                service:
                pinyin:
                environment:
                flavor:
              }
        words: a list of word phrases in one review

    output:
        priors: prior probability
        posteriors: posterior probability
    """
    global priors, posteriors, aspect, voc
    if data[aspect]:
        if data[aspect] > 2:
            rate = 1
        elif data[aspect] < 2:
            rate = 0
        else:
            # ignore review whose rating is 3
            return

        priors[rate] += 1
        for word in words:
            # [1] is for add-one smoothing purpose
            if word in voc:
                word = voc[word]
            else:
                tokenid = len(voc)
                voc[word] = tokenid
                word = tokenid
                posteriors.append([1, 1])
            posteriors[word][rate] += 1


def calc_prob():
    global priors, posteriors
    # calculate logarithmic prior probability
    rate_num = sum(priors)
    for i in range(len(priors)):
        priors[i] = math.log(priors[i]) - math.log(rate_num)

    # add one smoothing
    # for key in posteriors:
    #     for word in posteriors[key]:
    #         flag = 0
    #         for i in range(len(posteriors[key][word])):
    #             if posteriors[key][word][i] == 0:
    #                 flag = 1
    #                 break
    #         if flag == 1:
    #             posteriors[key][word] = map(
    #                 posteriors[key][word], lambda x: x + 1)

    # calculate logarithmic posterior probability
    for i in range(2):
        rate_num = 0
        for j in range(len(posteriors)):
            rate_num += posteriors[j][i]
        for j in range(len(posteriors)):
            posteriors[j][i] = math.log(
                posteriors[j][i]) - math.log(rate_num)


def learn(f):
    global priors, posteriors, c, feature, n_gram
    for line in f:
        c += 1
        json_data = json.loads(line, encoding="utf-8")
        if feature == 0:
            words = json_data["segmentation"].split("/")
        elif feature == 1:
            words = json_data["pinyin"].split("/")
        elif feature == 2:
            words = json_data["segmentation"].split(
                "/") + json_data["pinyin"].split("/")
        tokens = []
        if n_gram == 1:
            tokens = words
        elif n_gram == 2:
            for i in range(len(words) - 1):
                tokens.append(words[i] + words[i + 1])
        elif n_gram == 3:
            for i in range(len(words) - 2):
                tokens.append(words[i] +
                              words[i + 1] + words[i + 2])
        learn_one(json_data, tokens)


def main():
    global c, aspect, n_gram, feature, priors, posteriors, voc
    reload(sys)
    sys.setdefaultencoding('utf-8')
    pathname = sys.argv[1]
    n_gram = int(sys.argv[2])
    feature = int(sys.argv[3])
    aspect = sys.argv[4]

    i = 0
    files = glob.glob(pathname + "/*.txt")
    for train_file in files:
        with open(train_file, "r") as f:
            learn(f)
            i += 1
            print c, float(i) / len(files)
    calc_prob()
    model_name = str(n_gram) + "_" + str(feature) + "_" + aspect
    print "dump"
    with open(model_name, "w") as f:
        pickle.dump(priors, f)
        pickle.dump(len(posteriors), f)
        pickle.dump(voc, f)

        i = 0
        for value in posteriors:
            pickle.dump(value, f)
            if i % 100000 == 0:
                print str(i) + " ",
            i += 1
        print ""
        # pickle.dump(voc, f)
        # pickle.dump(posteriors, f)

if __name__ == "__main__":
    main()
