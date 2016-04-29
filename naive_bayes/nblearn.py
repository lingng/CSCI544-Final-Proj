#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import math
import json
import pickle

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


def learn_one(aspect, data, words):
    global priors, posteriors
    if data[aspect]:
        priors[aspect][data[aspect]] += 1
        for word in words:
            # [1] is for add-one smoothing purpose
            posteriors[aspect].setdefault(word, [0.1] * 5)
            posteriors[aspect][word][data[aspect]] += 1


def calc_prob():
    global priors, posteriors
    # calculate logarithmic prior probability
    for key in priors:
        rate_num = sum(priors[key])
        for i in range(len(priors[key])):
            priors[key][i] = math.log(
                priors[key][i] + 1) - math.log(rate_num + 5)

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
        for i in range(5):
            rate_num = 0
            for word in posteriors[key]:
                rate_num += posteriors[key][word][i]
            for word in posteriors[key]:
                posteriors[key][word][i] = math.log(
                    posteriors[key][word][i]) - math.log(rate_num)


def learn(file):
    global priors, posteriors
    c = 0
    for line in file:
        # print c
        c += 1
        json_data = json.loads(line, encoding="utf-8")
        words = json_data["segmentation"].split("/")
        learn_one("service", json_data, words)
        print posteriors["service"]
        learn_one("environment", json_data, words)
        learn_one("flavor", json_data, words)
    calc_prob()


def main():
    pathname = sys.argv[1]
    with open(pathname, "r") as f:
        learn(f)
    with open("nbmodel.txt", "w") as f:
        pickle.dump(priors, f)
        pickle.dump(posteriors, f)


if __name__ == "__main__":
    main()
