import pandas as pd
import filecmp

data_dir = r'../../Data/En/'
orig_dir = r'./orig_data/'

Ngram_count_start_from_question = 23

test_files= [r'Stem-Discr-Frq-Bigram-Question.csv', r'Stem-Discr-Frq-Trigram-Question.csv']

df_ac_bigram_q = pd.read_csv(data_dir +r'Bigram-Question.csv')
df_ac_bigram_q = df_ac_bigram_q.set_index('AC_Doc_ID')
df_ac_bigram_q_buf = df_ac_bigram_q.iloc[:, (Ngram_count_start_from_question - 1):]

df_ac_bigram_q_buf['Avg_Score'] = df_ac_bigram_q['Avg_Score']
df_ac_bigram_q_buf['Pre_Col_Name'] = df_ac_bigram_q['Pre_Col_Name']
df_ac_bigram_q_buf = df_ac_bigram_q_buf.fillna(0)
df_ac_bigram_q_buf_stem = df_ac_bigram_q_buf[df_ac_bigram_q_buf['Pre_Col_Name'].isin(['Stem'])]

df_ac_stem_discr = pd.DataFrame({ 'Bigram_sum' : df_ac_bigram_q_buf_stem.sum() })

df_corr = df_ac_bigram_q_buf_stem.corr()
df_ac_stem_discr['Corr_Avg_Score'] = df_corr['Avg_Score']

df_ac_stem_discr = df_ac_stem_discr.drop(['Pre_Col_Name', 'Avg_Score'])
df_ac_stem_discr.index.name = 'Bigram'
df_ac_stem_discr = df_ac_stem_discr.sort_values('Corr_Avg_Score')
df_ac_stem_discr.to_csv(data_dir +test_files[0])

df_ac_trigram_q = pd.read_csv(data_dir +r'Trigram-Question.csv')
df_ac_trigram_q = df_ac_trigram_q.set_index('AC_Doc_ID')
df_ac_trigram_q_buf = df_ac_trigram_q.iloc[:, (Ngram_count_start_from_question - 1):]

df_ac_trigram_q_buf['Avg_Score'] = df_ac_trigram_q['Avg_Score']
df_ac_trigram_q_buf['Pre_Col_Name'] = df_ac_trigram_q['Pre_Col_Name']
df_ac_trigram_q_buf = df_ac_trigram_q_buf.fillna(0)
df_ac_trigram_q_buf_stem = df_ac_trigram_q_buf[df_ac_trigram_q_buf['Pre_Col_Name'].isin(['Stem'])]

df_ac_stem_discr = pd.DataFrame({ 'Trigram_sum' : df_ac_trigram_q_buf_stem.sum() })

df_corr = df_ac_trigram_q_buf_stem.corr()
df_ac_stem_discr['Corr_Avg_Score'] = df_corr['Avg_Score']

df_ac_stem_discr = df_ac_stem_discr.drop(['Pre_Col_Name', 'Avg_Score'])
df_ac_stem_discr.index.name = 'Trigram'
df_ac_stem_discr = df_ac_stem_discr.sort_values('Corr_Avg_Score')
df_ac_stem_discr.to_csv(data_dir +test_files[1])

from file_cmp_diff_ratio import *

for x in test_files:
    file_cmp_diff_ratio(data_dir + x, orig_dir + x)
