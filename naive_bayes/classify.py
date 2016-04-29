#! /usr/bin/env python
# -*- coding: utf-8 -*-

try:
    import cPickle as pickle
except:
    import pickle
import json
import sys

import copy
import glob

feature = None  # 0 phrases only, 1 pinyin only, 2 mixed
n_gram = None
aspect = None

priors = [0, 0]
posteriors = []
voc = {}

def classify(w):
    global priors, posteriors, voc
    score = copy.deepcopy(priors)
    for t in w:
        if t in voc:
            t = voc[t]
            for c in range(2):
                score[c] += posteriors[t][c]
        else:
            pass
            # print "no %s\n" % t
    max_c = score.index(max(score))   # argmax
    return max_c


def main():
    global priors, posteriors, feature, n_gram, aspect, voc
    reload(sys)
    sys.setdefaultencoding('utf-8')
    model_name = sys.argv[2]
    config = model_name.split("_")

    n_gram = int(config[0])
    feature = int(config[1])
    aspect = config[2]

    with open(model_name, "r") as f:
        priors = pickle.load(f)
        num = pickle.load(f)
        voc = pickle.load(f)
        for i in range(num):
            posteriors.append(pickle.load(f))
            if i % 10000 == 0:
                print str(i) + " ",
        print ""

    target_dir = sys.argv[1]
    pathnames = glob.glob(target_dir + "/*.txt")
    counts = [0, 0, 0, 0]
    total_num = 0
    for pathname in pathnames:
        with open(pathname, "r") as f:
            for line in f:
                data = json.loads(line, encoding='utf-8')
                words = []
                if feature == 0:
                    words = data["segmentation"].split("/")
                elif feature == 1:
                    words = data["pinyin"].split("/")
                elif feature == 2:
                    words = data["segmentation"].split(
                        "/") + data["pinyin"].split("/")

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

                max_c = classify(tokens)

                if data[aspect] > 2:
                    ref_rate = 1
                elif data[aspect] < 2:
                    ref_rate = 0
                else:
                    continue

                if max_c == 1 and ref_rate == 1:
                    # true positive
                    counts[0] += 1
                elif max_c == 1 and ref_rate == 0:
                    # false positive
                    counts[1] += 1
                elif max_c == 0 and ref_rate == 1:
                    # true negative
                    counts[2] += 1
                elif max_c == 0 and ref_rate == 0:
                    # false negative
                    counts[3] += 1
                total_num += 1
        print counts
    with open("log1.txt", "w") as fout:
        fout.write("%d %d %d %d\n" % (counts[0], counts[1], counts[2], counts[3]))
        fout.write("\n")
    # print counts
        p = counts[0] / float(counts[0] + counts[1])
        recall = counts[0] / float(counts[0] + counts[2])
        # print model_name
        fout.write(model_name + "\n")
        # print "Accuracy: %f" % ((counts[0] + counts[3]) / float(total_num))
        # print "F1: %f" % (2 * p * recall / (p + recall))
        fout.write("Accuracy: %f\n" % ((counts[0] + counts[3]) / float(total_num)))
        fout.write("F1: %f\n" % (2 * p * recall / (p + recall)))

if __name__ == "__main__":
    main()
