import pandas as pd
import numpy as np
import filecmp

data_dir = r'../../Data/En/'
orig_dir = r'./orig_data/'

from ac_bi_trigram_pmi_distribution import *

Ngram_count_start_from_question = 23
Decimal_places = 4

test_file = r'PMI-Distribution-Bigram-Question.csv'

df_ac_bigram_q = pd.read_csv(data_dir + r'Bigram-Question.csv')
df_ac_bigram_q = df_ac_bigram_q.set_index('AC_Doc_ID')

df_ac_pmi_bigram = pd.read_csv(data_dir + 'PMI-Sum-T-Bigram-Passage.csv')

df_ac_bigram_q_buf_pmi = ac_bi_trigram_pmi_distribution(df_ac_bigram_q, Ngram_count_start_from_question - 1, 
                             df_ac_pmi_bigram, 'bigram', Decimal_places)

df_ac_bigram_q_buf_pmi.to_csv(data_dir + test_file)

from file_cmp_diff_ratio import *

file_cmp_diff_ratio(data_dir + test_file, orig_dir + test_file) 
