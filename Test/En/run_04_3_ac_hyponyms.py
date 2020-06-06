import pandas as pd
import filecmp

from ac_hyponyms import *

data_dir = r'../../Data/En/'
orig_dir = r'./orig_data/'

lemma_count_start_from_question = 23
lemma_count_start_from_passage = 5

test_files= [r'Hyponyms-Question.csv', r'Hyponyms-Passage.csv']

df_ac_lemma_q = pd.read_csv(data_dir + r'Lemma-Question.csv')
df_ac_lemma_q = df_ac_lemma_q.set_index('AC_Doc_ID')

df_ac_lemma_q_loc = df_ac_lemma_q.iloc[:,0:(lemma_count_start_from_question - 1)]
df_ac_hyponyms = ac_hyponyms(df_ac_lemma_q_loc,'Cntnt_Lemma')
df_ac_hyponyms = df_ac_hyponyms.drop(['Cntnt_Lemma'], axis=1)
df_ac_hyponyms.to_csv(data_dir + test_files[0])

df_ac_lemma_p = pd.read_csv(data_dir + r'Lemma-Passage.csv')
df_ac_lemma_p = df_ac_lemma_p.set_index('AC_Doc_ID')

df_ac_lemma_p_loc = df_ac_lemma_p.iloc[:,0:(lemma_count_start_from_passage - 1)]
df_ac_hyponyms_p = ac_hyponyms(df_ac_lemma_p_loc,'Cntnt_Lemma')
df_ac_hyponyms_p = df_ac_hyponyms_p.drop(['Cntnt_Lemma'], axis=1)
df_ac_hyponyms_p.to_csv(data_dir + test_files[1])

from file_cmp_diff_ratio import *

for x in test_files:
    file_cmp_diff_ratio(data_dir + x, orig_dir + x)
