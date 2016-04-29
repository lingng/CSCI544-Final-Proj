import sys
from liblinearutil import *
from format_data import *          

def main(option_s, option_e, N_s, N_e, setting_s, setting_e):
    option_tag = ['service_', 'environment_', 'flavor_', '']
    ngram_tag = ['unigram_', 'bigram_', 'trigram_']
    setting_tag = ['chinese_only_', 'pinyin_only_', 'chinese_pinyin_']
    parent_dir = os.path.dirname(os.path.abspath(os.curdir) )
    for option in xrange(option_s, option_e):
        for setting in xrange(setting_s, setting_e):
            for N in xrange(N_s, N_e):
                model_id = 'svm_model(150)_' + option_tag[option-1]+ngram_tag[N-1]+setting_tag[setting-1] + '.model'
                print 'Load model %s...' % model_id
                m = load_model(model_id)
                input_file_name = 'testing_input_'+option_tag[option-1]+ngram_tag[N-1]+setting_tag[setting-1]+'.txt'
                input_file_path = os.path.join(parent_dir, input_file_name )
                output_dir = os.path.join(parent_dir, 'prediction_output')
                print 'predicting file %s...' % input_file_path
                trueLabels, feature_vectors = readDataFromFile(input_file_path)
                p_labs, p_acc, p_vals = predict(trueLabels, feature_vectors, m)
                fileName = os.path.join(output_dir, 'prediction_'+input_file_name )
                print 'outputting to file %s...' % fileName
                with open(fileName, 'w') as outfile:                    
                    for index, value in enumerate(p_labs):
                        outfile.write('Predict=%s\tTrueLabel=%s\n'%(value, trueLabels[index]))
if __name__ == '__main__':
    option_s = 3
    option_e = option_s+1
    N_s = 1
    N_e = N_s+1
    setting_s = 3
    setting_e = setting_s+1
    main(option_s, option_e, N_s, N_e, setting_s, setting_e)