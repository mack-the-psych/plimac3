import filecmp

from semi_structured_ac_text_parser import *

data_dir = r'../../Data/En/'
orig_dir = r'./orig_data/'

colNames = ['Question', 'Stem', 'A.', 'B.', 'C.', 'D.', 'EndQ']
test_file = r'ContentMatix-Question-NAEP-G8-Reading-92-13.csv'

dfQuestion = semi_structured_ac_text_parser(data_dir + r'Question-NAEP-G8-Reading-92-13.txt', colNames)
dfQuestion.to_csv(data_dir + test_file)

from file_cmp_diff_ratio import *

file_cmp_diff_ratio(data_dir + test_file, orig_dir + test_file)
