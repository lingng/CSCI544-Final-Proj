import sys
import numpy as py
import json
from svmutil import *

def parseJson(file):
    dict = {}
    with open(file, 'r') as doc:
        index = 0
        for line in doc:
            dict[index] = (json.loads(line.strip()) )
            index += 1
    return dict    

data = parseJson(sys.argv[1])
 
        