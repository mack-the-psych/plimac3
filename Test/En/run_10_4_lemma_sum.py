import pandas as pd
import math
import filecmp

data_dir = r'../../Data/En/'
orig_dir = r'./orig_data/'

Lemma_count_start_from_question = 23
Lemma_count_start_from_passage = 5

test_files= [r'Sum-T-Lemma-Question.csv', r'Sum-T-Lemma-Question-Stem.csv', 
             r'Sum-T-Lemma-Passage.csv']

df_ac_lemma_q = pd.read_csv(data_dir +r'Lemma-Question.csv')
df_ac_lemma_q = df_ac_lemma_q.set_index('AC_Doc_ID')

df_ac_lemma_q_buf = df_ac_lemma_q.iloc[:, (Lemma_count_start_from_question -1):]
df_ac_lemma_q_res = pd.DataFrame({ 'Lemma_sum' : df_ac_lemma_q_buf.sum() })
df_ac_lemma_q_res = pd.concat([df_ac_lemma_q_res, df_ac_lemma_q_buf.transpose()], axis = 1)
df_ac_lemma_q_res = df_ac_lemma_q_res.sort_values('Lemma_sum', ascending=False)
df_ac_lemma_q_res.to_csv(data_dir +test_files[0])

df_ac_lemma_q_buf = df_ac_lemma_q[df_ac_lemma_q['Pre_Col_Name'].isin(['Stem'])]
df_ac_lemma_q_buf = df_ac_lemma_q_buf.iloc[:, (Lemma_count_start_from_question -1):]
df_ac_lemma_q_res = pd.DataFrame({ 'Lemma_sum' : df_ac_lemma_q_buf.sum() })
df_ac_lemma_q_res = pd.concat([df_ac_lemma_q_res, df_ac_lemma_q_buf.transpose()], axis = 1)
df_ac_lemma_q_res = df_ac_lemma_q_res.sort_values('Lemma_sum', ascending=False)
df_ac_lemma_q_res = df_ac_lemma_q_res[df_ac_lemma_q_res['Lemma_sum'] >= 1]
df_ac_lemma_q_res.to_csv(data_dir +test_files[1])

df_ac_lemma_p = pd.read_csv(data_dir +r'Lemma-Passage.csv')
df_ac_lemma_p = df_ac_lemma_p.set_index('AC_Doc_ID')

df_ac_lemma_p_buf = df_ac_lemma_p.iloc[:, (Lemma_count_start_from_passage -1):]
df_ac_lemma_p_res = pd.DataFrame({ 'Lemma_sum' : df_ac_lemma_p_buf.sum() })
df_ac_lemma_p_res = pd.concat([df_ac_lemma_p_res, df_ac_lemma_p_buf.transpose()], axis = 1)
df_ac_lemma_p_res = df_ac_lemma_p_res.sort_values('Lemma_sum', ascending=False)
df_ac_lemma_p_res.to_csv(data_dir +test_files[2])

from file_cmp_diff_ratio import *

for x in test_files:
    file_cmp_diff_ratio(data_dir + x, orig_dir + x)
