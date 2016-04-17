import sys
import numpy as py
import json
from svmutil import *

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

def getXYArray(setting):    
    #stopWords = set(readStopWordList('Chinese_stopwords.txt') )
    labels = []
    feature_vectors = []
    feature = {}
    dict = parseJson(sys.argv[1])
    for key in dict:
        label = str(dict[key]['service'])+str(dict[key]['environment'])+str(dict[key]['flavor'])
        my_feature = {}
        for i in xrange(1, 4):
            fV = getNgramFVWithSetting(dict[key], setting, i)
            for f in fV:
                #if fV[f] == 1:
                #    continue
                if f not in feature:    #new feature, assign this feature a number and record its numerical value
                    value = len(feature)
                    feature[f] = value
                    my_feature[value] = fV[f]
                else:   #existing feature, find its assigned number and record its numerical value
                    my_feature[feature[f]] = fV[f]
        labels.append(label)
        feature_vectors.append(my_feature)
    """
    for key in feature:
        print decodeUTF8(key), feature[key]
       
    for index, element in enumerate(labels):
        print element, feature_vectors[index]
    """            
    return labels, feature_vectors, feature
def joinDictionaryString(dict):
    temp = []
    for i in dict.items():
        current = ':'.join(str(x) for x in i)
        temp.append(current)
    return ' '.join(temp)    
if __name__ == "__main__":
    labels, feature_vectors, mapping = getXYArray(int(sys.argv[2])) 
    with open('svm_training_input_' + sys.argv[2] + '.txt', 'w') as file:
        for index, element in enumerate(labels):
            file.write(str(element) + ' ' + joinDictionaryString(feature_vectors[index]) + '\n')   
    with open('feature_mapping_' + sys.argv[2] + '.txt', 'w') as file:
        for key in mapping:
            file.write(decodeUTF8(key)+':'+ str(mapping[key])+'\n');   
    