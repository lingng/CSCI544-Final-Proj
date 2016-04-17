import sys
import ast
import numpy as py
import json
from svmutil import *
from format_data import *

def main(i):
    fileName = 'svm_training_input_'+i+'.txt'
    labels, feature_vectors = readDataFromFile(fileName)
    prob = svm_problem(labels, feature_vectors)
    param = svm_parameter()
    m = svm_train(prob, param)
    svm_save_model('svm_model_'+i+'.model', m)
    
if __name__ == "__main__":
    for i in xrange(1,4):
        main(i)
 
        