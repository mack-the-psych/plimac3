import pandas as pd
import filecmp

from ac_bi_trigram import *

data_dir = r'../../Data/En/'
orig_dir = r'./orig_data/'

test_files= [r'Bigram-Passage.csv', r'Trigram-Passage.csv']

df_ac_p = pd.read_csv(data_dir +r'Manual_Edit-ContentMatix-Reading Passage-NAEP-G8-Reading-92-13.csv')

df_ac_bigram_p = ac_bi_trigram(df_ac_p,'Content')
df_ac_bigram_p.to_csv(data_dir +test_files[0])

df_ac_trigram_p = ac_bi_trigram(df_ac_p,'Content', 'trigram')
df_ac_trigram_p.to_csv(data_dir +test_files[1])

from file_cmp_diff_ratio import *

for x in test_files:
    file_cmp_diff_ratio(data_dir + x, orig_dir + x)
