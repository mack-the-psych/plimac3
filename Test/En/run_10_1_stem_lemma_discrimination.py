import pandas as pd
import filecmp

data_dir = r'../../Data/En/'
orig_dir = r'./orig_data/'

Lemma_count_start_from_question = 23

test_file = r'Stem-Discr-Frq-Lemma-Question.csv'

df_ac_lemma_q = pd.read_csv(data_dir +r'Lemma-Question.csv')
df_ac_lemma_q = df_ac_lemma_q.set_index('AC_Doc_ID')
df_ac_lemma_q_buf = df_ac_lemma_q.iloc[:, (Lemma_count_start_from_question - 1):]

df_ac_lemma_q_buf['Avg_Score'] = df_ac_lemma_q['Avg_Score']
df_ac_lemma_q_buf['Pre_Col_Name'] = df_ac_lemma_q['Pre_Col_Name']
df_ac_lemma_q_buf = df_ac_lemma_q_buf.fillna(0)
df_ac_lemma_q_buf_stem = df_ac_lemma_q_buf[df_ac_lemma_q_buf['Pre_Col_Name'].isin(['Stem'])]

df_ac_stem_discr = pd.DataFrame({ 'Lemma_sum' : df_ac_lemma_q_buf_stem.sum() })

df_corr = df_ac_lemma_q_buf_stem.corr()
df_ac_stem_discr['Corr_Avg_Score'] = df_corr['Avg_Score']

df_ac_stem_discr = df_ac_stem_discr.drop(['Pre_Col_Name', 'Avg_Score'])
df_ac_stem_discr.index.name = 'Lemma'
df_ac_stem_discr = df_ac_stem_discr.sort_values(by=['Corr_Avg_Score'])
df_ac_stem_discr.to_csv(data_dir +test_file)

from file_cmp_diff_ratio import *

file_cmp_diff_ratio(data_dir + test_file, orig_dir + test_file)
