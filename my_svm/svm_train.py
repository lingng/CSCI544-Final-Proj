import sys
import ast
import numpy as py
import json
from svmutil import *
from format_data import *

def main(i, option):
    #option = 3
    option_tag = ['service_', 'environment_', 'flavor_', '']
    
    fileName = 'svm_training_input_' +option_tag[option-1] +str(i)+'.txt'
    labels, feature_vectors = readDataFromFile(fileName)
    prob = svm_problem(labels, feature_vectors)
    param = svm_parameter('-s 0 -t 2 -c 10 -h 0')
    m = svm_train(prob, param)
    svm_save_model('svm_model_' +option_tag[option-1] +str(i)+'.model', m)
    
if __name__ == "__main__":
    """
    for i in xrange(1,4):
        for option in xrange(1, 4):
            print 'Training setting ', i, '...:'
            main(i, option)
    """
    main(3, 1)
        