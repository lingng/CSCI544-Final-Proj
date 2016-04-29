#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import math
import json
import pickle
import glob

_feature = 2  # 0 phrases only, 1 pinyin only, 2 mixed
_ngram = 1
c = 0

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


def learn_one(aspect, data, words):
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
    global priors, posteriors
    if data[aspect]:
        if data[aspect] > 2:
            rate = 1
        elif data[aspect] < 2:
            rate = 0
        else:
            # ignore review whose rating is 3
            return

        priors[aspect][rate] += 1
        for word in words:
            # [1] is for add-one smoothing purpose
            posteriors[aspect].setdefault(word, [1] * _class_num)
            posteriors[aspect][word][rate] += 1


def calc_prob():
    global priors, posteriors
    # calculate logarithmic prior probability
    for key in priors:
        rate_num = sum(priors[key])
        for i in range(len(priors[key])):
            priors[key][i] = math.log(priors[key][i]) - math.log(rate_num)

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
    for key in posteriors:
        for i in range(_class_num):
            rate_num = 0
            for word in posteriors[key]:
                rate_num += posteriors[key][word][i]
            for word in posteriors[key]:
                posteriors[key][word][i] = math.log(
                    posteriors[key][word][i]) - math.log(rate_num)


def learn(file):
    global priors, posteriors, c
    for line in file:
        c += 1
        json_data = json.loads(line, encoding="utf-8")

        if _feature == 0:
            words = json_data["segmentation"].split("/")
        elif _feature == 1:
            words = json_data["pinyin"].split("/")
        elif _feature == 2:
            words = json_data["segmentation"].split(
                "/") + json_data["pinyin"].split("/")
        ngrams = []
        if _ngram == 1:
            ngrams = words
        elif _ngram == 2:
            for i in range(len(words) - 1):
                ngrams.append(words[i] + "_" + words[i + 1])
        elif _ngram == 3:
            for i in range(len(words) - 2):
                ngrams.append(words[i] + "_" +
                              words[i + 1] + "_" + words[i + 2])
        learn_one("service", json_data, ngrams)
        # print posteriors["service"]
        learn_one("environment", json_data, ngrams)
        learn_one("flavor", json_data, ngrams)


def main():
    global c
    pathname = sys.argv[1]
    files = glob.glob(pathname + "/*.txt")
    # print files

    i = 0
    for train_file in files:
        with open(train_file, "r") as f:
            learn(f)
            i += 1
            print c, float(i) / len(files)
    calc_prob()
    with open(sys.argv[2], "w") as f:
        pickle.dump(priors, f)
        pickle.dump(posteriors, f)
        pickle.dump(_feature, f)
        pickle.dump(_ngram, f)


if __name__ == "__main__":
    main()
