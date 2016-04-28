import sys
import os
import pickle
import json
from format_data import *

ngram_tag = ['unigram_', 'bigram_', 'trigram_']
setting_tag = ['chinese_only_', 'pinyin_only_', 'chinese_pinyin_']

def main(N, setting):
    parent_dir = os.path.dirname(os.path.abspath(os.curdir) )
    archive_path = os.path.join(parent_dir, 'Archive')
    features = {}
    for dirPath, dirNames, fileNames in os.walk(archive_path):
        for f in fileNames:
            if not '.txt' in f:
                continue
            current_f_path = os.path.join(dirPath, f)
            current_json_dict = parseJson(current_f_path)
            for key in current_json_dict:
                for N in xrange(N, N+1): 
                    fV = getNgramFVWithSetting(current_json_dict[key], setting, N)
                    for feature in fV:
                        if len(feature) < 1:
                            continue
                        if feature not in features:
                            value = len(features)
                            features[feature] = value
    
    
    print 'Number of features for setting /"%s/" = %s' % (setting_tag[setting-1], len(features) )
    with open('feature_dict_'+ngram_tag[N-1] + setting_tag[setting-1]+'.pickle', 'w') as outfile:
        pickle.dump(features, outfile)    

def test():
    for N in xrange(1, 4):
        for setting in xrange(1, 4):
            with open('feature_dict_'+ngram_tag[N-1] + setting_tag[setting-1]+'.pickle', 'r') as infile:
                features = pickle.load(infile)
                print 'file: %s, size = %s' % (infile, len(features))

if __name__ == '__main__':
    for setting in xrange(1, 4):
        for N in xrange(1, 4):
            main(N, setting)