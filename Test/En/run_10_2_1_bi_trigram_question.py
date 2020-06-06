import pandas as pd
import filecmp

from ac_bi_trigram import *

data_dir = r'../../Data/En/'
orig_dir = r'./orig_data/'

test_files= [r'Bigram-Question.csv', r'Trigram-Question.csv']

df_ac_q = pd.read_csv(data_dir +r'Serialized-Manual_Edit-ContentMatix-Question-NAEP-G8-Reading-92-13.csv')

df_ac_bigram_q = ac_bi_trigram(df_ac_q,'Content')
df_ac_bigram_q.to_csv(data_dir +test_files[0])

df_ac_trigram_q = ac_bi_trigram(df_ac_q,'Content', 'trigram')
df_ac_trigram_q.to_csv(data_dir +test_files[1])

from file_cmp_diff_ratio import *

for x in test_files:
    file_cmp_diff_ratio(data_dir + x, orig_dir + x)
