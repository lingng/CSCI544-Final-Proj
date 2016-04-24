import sys
import ast
import numpy as py
import json
import pickle
from liblinearutil import *
from format_data import *

def main():
    #option = 3
    option_tag = ['_service', '_environment', '_flavor']
    ngram_tag = ['unigram_', 'bigram_', 'trigram_']
    setting_tag = ['chinese_only_', 'pinyin_only_', 'chinese_pinyin_']
    parent_dir = os.path.dirname(os.path.abspath(os.curdir) )
    for option in xrange(2, 4):
        working_dir = os.path.join(parent_dir, 'training'+option_tag[option-1])
        
        for setting in xrange(1, 4):
            for N in xrange(1, 4):
                labels = []
                feature_vectors = []
                for dirPath, dirNames, fileNames in os.walk(os.path.join(parent_dir, 'Archive')):
                    for index, f in enumerate(fileNames):
                        if not '.txt' in f:
                            continue
                        if index >= 85:
                            break
                        temp_f_name = f.replace('.txt', '_')+ngram_tag[N-1]+setting_tag[setting-1]+'.txt'
                        current_file = os.path.join(working_dir, temp_f_name)
                        print 'loading file %s...' % current_file
                        temp_labels, temp_feature_vectors = readDataFromFile(current_file)
                        labels.extend(temp_labels)
                        feature_vectors.extend(temp_feature_vectors)
                print 'setting up problem...'
                prob = problem(labels, feature_vectors)
                print 'setting up parameter...'
                param = parameter()
                print 'training...'
                m = train(prob, param)
                print 'saving...'
                save_model('svm_model_'+option_tag[option-1]+'_'+ngram_tag[N-1]+setting_tag[setting-1]+'.model', m)
    
if __name__ == "__main__":
    main()
        