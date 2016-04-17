import sys
from svmutil import *
from format_data import *

def readFeatureFromFile(path):
    output = {}
    with open(path, 'r') as file:
        for line in file:
            line = line.strip()
            tokens = line.split(':')
            if len(tokens) < 2:
                continue
            output[tokens[0]] = tokens[1]
    return output

def convertData(setting):
    feature_file = 'feature_mapping_'+setting+'.txt'
    feature = readFeatureFromFile(feature_file)
    dict = parseJson(sys.argv[1])
    labels = []
    feature_vectors = []
    for key in dict:
        label = str(dict[key]['service']+1)+str(dict[key]['environment']+1)+str(dict[key]['flavor']+1)
        my_feature = {}
        for i in xrange(1, 4):
            fV = getNgramFVWithSetting(dict[key], setting, i)
            for f in fV:
                #if fV[f] == 1:
                #    continue
                if f not in feature:    #unseen feature, skip
                    continue
                else:   #existing feature, find its assigned number and record its numerical value
                    my_feature[int(feature[f])] = fV[f]
        labels.append(int(label))
        feature_vectors.append(my_feature)
    return labels, feature_vectors

def outputToFile(path, labels, feature_vectors):
    with open(path, 'w') as file:
        for index, element in enumerate(labels):
            file.write(str(element) + ' ' + joinDictionaryString(feature_vectors[index]) + '\n') 
            
def generatePredictFile():
    trueLabels, feature_vectors = convertData(sys.argv[2])
    outputToFile('svm_predict_input_'+sys.argv[2]+'.txt', trueLabels, feature_vectors)

def main():
    m = svm_load_model('svm_model_' + sys.argv[2] + '.model')
    fileName = 'svm_predict_input_'+sys.argv[2]+'.txt'
    trueLabels, feature_vectors = readDataFromFile(fileName)
    p_labs, p_acc, p_vals = svm_predict(trueLabels, feature_vectors, m)
    print trueLabels
    print p_labs
    print p_acc
    with open('prediction_output_'+sys.argv[2]+'.txt', 'w') as outfile:
        for index, value in enumerate(p_labs):
            outfile.write('Predict=%s\tTrueLabel=%s\n'%(value, trueLabels[index]))
if __name__ == '__main__':
    """
    argv = [inputfile, setting]
    """
    generatePredictFile()
    #main()