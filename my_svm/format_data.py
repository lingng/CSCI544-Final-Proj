import sys
import os
import pickle
import numpy as py
import json
import ast
from svmutil import *
from pickle import NONE

def readStopWordList(filePath):
    output = []
    with open(filePath, 'r') as file:
        for line in file:
            line = line.strip()
            if line not in output:
                output.append(line)
    return output

def parseJson(file):
    dict = {}
    with open(file, 'r') as doc:
        index = 0
        for line in doc:
            dict[index] = (json.loads(line.strip()) )
            index += 1
    return dict    

def removeStopWord(line, stopWords):
    tokens = line.strip().split('/')
    output = []
    for i in tokens:
        if i in stopWords:
            continue
        output.append(i)
    return output
    
def getNgramFV(line, N):
    output = {}
    #tokens = removeStopWord(line, stopWords)
    tokens = line.strip().split('/')
    ngrams = zip(*[tokens[i:] for i in range(N)])
    for element in ngrams:
        temp = element[0]
        if temp not in output:
            output[temp] = 1
        else:
            output[temp] += 1
    return output

def getCombinedNgramFV(line1, line2, N):
    output = {}
    tokens1 = line1.strip().split('/')
    tokens2 = line2.strip().split('/')
    ngrams1 = zip(*[tokens1[i:] for i in range(N)])
    ngrams2 = zip(*[tokens2[i:] for i in range(N)])
    for index, element in enumerate(ngrams1):
        temp = element[0]+ngrams2[index][0]
        #print element[0].encode('utf-8')+ngrams2[index][0].encode('utf-8')
        if temp not in output:
            output[temp] = 1
        else:
            output[temp] += 1
    return output 
    
def getNgramFVWithSetting(data, setting, N):
    """
    Setting 1 = raw Chinese Characters
    Setting 2 = raw Pinyin
    Setting 3 = Chinese Characters + Pinyin
    """
    if setting == 1:
        return getNgramFV(data['segmentation'], N)
    elif setting == 2:
        return getNgramFV(data['pinyin'], N)
    else:
        return getCombinedNgramFV(data['segmentation'], data['pinyin'], N)
    
def decodeUTF8(key_tuple):
    return ''.join(x.encode('utf-8') for x in key_tuple)

def getXYArray(current_file, feature_dict, N, option, setting):    
    #stopWords = set(readStopWordList('Chinese_stopwords.txt') )
    option_tag = ['service', 'environment', 'flavor']
    labels = []
    feature_vectors = []
    dict = parseJson(current_file)
    for key in dict:    
        label = None
        temp = dict[key][option_tag[option-1]]    
        if temp < 2:
            label = -1
        if temp == 2:
            label = 0
        if temp > 2:
            label = 1
        my_feature = {}
        fV = getNgramFVWithSetting(dict[key], setting, N)
        for f in fV:
            if len(f)<1 or f not in feature_dict:
                continue
            my_feature[feature_dict[f]] = fV[f]
        labels.append(label)
        feature_vectors.append(my_feature)           
    return labels, feature_vectors
def joinDictionaryString(dict):
    temp = []
    for i in dict.items():
        current = ':'.join(str(x) for x in i)
        temp.append(current)
    return ' '.join(temp)  
def readDataFromFile(path):
    labels = []
    feature_vectors = []
    with open(path, 'r') as file:
        for line in file:
            line = line.strip();
            tokens = line.split(' ')
            labels.append(float(tokens[0]))
            feature_vectors.append( ast.literal_eval('{' + (', '.join(tokens[1:]) ) +'}') )
    return labels, feature_vectors

def load_feature(path):
    output = None
    with open(path, 'rb') as file:
        output = pickle.load(file)
    return output

def main():
    option_tag = ['_service', '_environment', '_flavor']
    ngram_tag = ['unigram_', 'bigram_', 'trigram_']
    setting_tag = ['chinese_only_', 'pinyin_only_', 'chinese_pinyin_']
    parent_dir = os.path.dirname(os.path.abspath(os.curdir) )
    for setting in xrange(1, 4):
        for N in xrange(1, 4):
            path = 'feature_dict_'+ngram_tag[N-1] + setting_tag[setting-1]+'.pickle'
            feature_dict = load_feature(path)
            archive_path = os.path.join(parent_dir, 'Testing')
            for dirPath, dirNames, fileNames in os.walk(archive_path):
                for f in fileNames:
                    if not '.txt' in f:
                        continue
                    current_file = os.path.join(dirPath, f)
                    for option in xrange(1, 4):
                        labels, feature_vectors = getXYArray(current_file, feature_dict, N, option, setting)
                        output_dir = os.path.join(parent_dir, 'testing'+option_tag[option-1])
                        temp_file_name = f.replace('.txt', '_') +ngram_tag[N-1] + setting_tag[setting-1] + '.txt'
                        output_path = os.path.join(output_dir, temp_file_name)
                        with open(output_path, 'w') as outfile:
                            for index, element in enumerate(labels):
                                outfile.write(str(element) + ' ' + joinDictionaryString(feature_vectors[index]) + '\n')
if __name__ == "__main__":
    main()
    