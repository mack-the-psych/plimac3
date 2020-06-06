import filecmp

from replace_where_for_ac_text_parser import *

data_dir = r'../../Data/En/'
orig_dir = r'./orig_data/'

words_replace_from = ['Quest', 'Stm']
words_replace_to = ['Question', 'Stem']
positions_where = [0, 0]
test_file = r'Question-NAEP-G8-Reading-92-13.txt'

replace_where_for_ac_text_parser(data_dir + r'Original-Question-NAEP-G8-Reading-92-13.txt', 
                        data_dir + test_file, words_replace_from, words_replace_to, positions_where)

from file_cmp_diff_ratio import *

file_cmp_diff_ratio(data_dir + test_file, orig_dir + test_file)
