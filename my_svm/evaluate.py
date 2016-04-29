import sys
import os

def list_dir(file_list):
    for index, element in enumerate(file_list):
        print ('%s. %s\t' % (index, element)),
        if index % 2 == 1:
            print
def evaluate_file(path):
    tp = 0
    tn= 0
    fp = 0
    fn = 0
    with open(path, 'r') as file:
        for line in file:
            if not 'Predict=' in line or 'TrueLabel=0.0' in line:
                continue
            if ('Predict=1.0' in line and 'TrueLabel=1.0' in line ):
                tp += 1
            elif ('Predict=-1.0' in line and 'TrueLabel=-1.0' in line):
                tn += 1
            elif ('Predict=1.0' in line and 'TrueLabel=-1.0' in line):
                fp += 1
            else:
                fn += 1
    
    print '(tp, tn, fp, fn) = (%s, %s, %s, %s)' % (tp, tn, fp, fn)
    precision = (float(tp)/float(tp+fp))
    recall = (float(tp)/float(tp+fn))
    F1 = 2*precision*recall/(precision+recall)
    accuracy = (float(tp+tn)/float(tp+tn+fp+fn))*100
    print 'precision = %s, recall = %s, F1 = %s' % (precision, recall, F1)
    print 'Accuracy (correct/total) = '+str(accuracy)+'%'
    
def main1():
    parent_dir = os.path.dirname(os.path.abspath(os.curdir) )
    predict_out_dir = os.path.join(parent_dir, 'prediction_output')
    file_list = []
    for f in os.listdir(predict_out_dir):
        if not '.txt' in f:
            continue
        file_list.append(f)
    while True:
        list_dir(file_list)
        option = raw_input('\nChoose a file index or enter \'Q\\q\' to quit:')
        if option == 'q' or option == 'Q':
            break
        elif int(option) >= len(file_list):
            print 'Invalid index.'
            continue
        else:
            evaluate_file(os.path.join(predict_out_dir, file_list[int(option)]) )

def main2():
    parent_dir = os.path.dirname(os.path.abspath(os.curdir) )
    predict_out_dir = os.path.join(parent_dir, 'prediction_output')
    for f in os.listdir(predict_out_dir):
        if not '.txt' in f:
            continue
        print f+':'
        evaluate_file(os.path.join(predict_out_dir, f) )
        print '---------------------------------------------------------------'
            

if __name__ == '__main__':
    main2()
