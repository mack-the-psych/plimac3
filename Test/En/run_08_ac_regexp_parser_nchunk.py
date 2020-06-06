import pandas as pd
import nltk
import filecmp

import ac_regexp_parser as rp

data_dir = r'../../Data/En/'
orig_dir = r'./orig_data/'

grammer = r'''
    NP: {<JJ|POS|CD|NN.*>+} # Chunk sequences of POS, JJ, NN
    '''

test_files= [r'Parsed-Question.csv', r'Parsed-Passage.csv']

df_ac_q = pd.read_csv(data_dir + r'Serialized-Manual_Edit-ContentMatix-Question-NAEP-G8-Reading-92-13.csv')
df_ac_nchunk_q = rp.ac_regexp_parser(df_ac_q, 'Content', grammer)
df_ac_nchunk_q.to_csv(data_dir + test_files[0])

df_ac_p = pd.read_csv(data_dir + r'Manual_Edit-ContentMatix-Reading Passage-NAEP-G8-Reading-92-13.csv')
df_ac_nchunk_p = rp.ac_regexp_parser(df_ac_p, 'Content', grammer)
df_ac_nchunk_p.to_csv(data_dir + test_files[1])

from file_cmp_diff_ratio import *

for x in test_files:
    file_cmp_diff_ratio(data_dir + x, orig_dir + x)
