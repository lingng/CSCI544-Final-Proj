import sys
import os

def main():
    option_tag = ['_service', '_environment', '_flavor']
    ngram_tag = ['unigram_', 'bigram_', 'trigram_']
    setting_tag = ['chinese_only_', 'pinyin_only_', 'chinese_pinyin_']
    parent_dir = os.path.dirname(os.path.abspath(os.curdir) )
    for option in xrange(1, 4):
        working_dir = os.path.join(parent_dir, 'training'+option_tag[option-1])        
        for setting in xrange(1, 4):
            for N in xrange(1, 4):
                output_path = os.path.join(parent_dir, 'training_input'+option_tag[option-1]+'_'+ngram_tag[N-1]+setting_tag[setting-1]+'.txt')
                with open(output_path, 'w') as outfile:
                    for dirPath, dirNames, fileNames in os.walk(os.path.join(parent_dir, 'Archive')):
                        for f in fileNames:
                            if not '.txt' in f:
                                continue
                            temp_f_name = f.replace('.txt', '_')+ngram_tag[N-1]+setting_tag[setting-1]+'.txt'
                            current_file = os.path.join(working_dir, temp_f_name)
                            print 'loading file %s...' % current_file
                            with open(current_file, 'r') as inputfile:
                                for line in inputfile:
                                    outfile.write(line)
                                    

if __name__ == '__main__':
    main()