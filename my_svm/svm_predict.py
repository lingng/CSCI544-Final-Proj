import sys
from liblinearutil import *
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

def convertData(setting, option):
    option_tag = ['service_', 'environment_', 'flavor_', '']
    feature_file = 'feature_mapping_'+option_tag[option-1]+str(setting)+'.txt'
    feature = readFeatureFromFile(feature_file)
    dict = parseJson(sys.argv[1])
    labels = []
    feature_vectors = []
    for key in dict:
        label = ''
        if option == 1:
            label = str(dict[key]['service']+1)
        if option == 2:
            label = str(dict[key]['environment']+1)
        if option == 3:
            label = str(dict[key]['flavor']+1)
        if option == 4:    
            label = str(dict[key]['service']+1)+str(dict[key]['environment']+1)+str(dict[key]['flavor']+1)
        my_feature = {}
        for i in xrange(1, 4):
            fV = getNgramFVWithSetting(dict[key], setting, i)
            for f in fV:
                #if fV[f] == 1:
                #    continue
                if f not in feature or len(f)<1:    #unseen feature, skip
                    continue
                else:   #existing feature, find its assigned number and record its numerical value
                    #print feature[f]
                    my_feature[int(feature[f])] = fV[f]
        labels.append(int(label))
        feature_vectors.append(my_feature)
    return labels, feature_vectors

def outputToFile(path, labels, feature_vectors):
    with open(path, 'w') as file:
        for index, element in enumerate(labels):
            file.write(str(element) + ' ' + joinDictionaryString(feature_vectors[index]) + '\n') 
            
def generatePredictFile(setting, option):
    option_tag = ['service_', 'environment_', 'flavor_', '']
    trueLabels, feature_vectors = convertData(setting, option)
    outputToFile('svm_predict_input_'+option_tag[option-1]+str(setting)+'.txt', trueLabels, feature_vectors)

def main(setting, option):
    option_tag = ['service_', 'environment_', 'flavor_', '']
    m = svm_load_model('svm_model_' + option_tag[option-1] + str(setting) + '.model')
    fileName = 'svm_predict_input_'+option_tag[option-1] + str(setting) +'.txt'
    trueLabels, feature_vectors = readDataFromFile(fileName)
    p_labs, p_acc, p_vals = svm_predict(trueLabels, feature_vectors, m)
    print trueLabels
    print p_labs
    print p_acc
    with open('prediction_output_'+option_tag[option-1] + str(setting)+'.txt', 'w') as outfile:
        for index, value in enumerate(p_labs):
            outfile.write('Predict=%s\tTrueLabel=%s\n'%(value, trueLabels[index]))
if __name__ == '__main__':
    """
    argv = [inputfile, setting]
    
    for i in xrange(1,4):
        for j in xrange(1,4):
            #generatePredictFile(i, j)
            main(i, j)
    """
    main(3, 1)