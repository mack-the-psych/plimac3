import pandas as pd
import filecmp

data_dir = r'../../Data/En/'
orig_dir = r'./orig_data/'

Ngram_count_start_from_question = 23

test_files= [r'Sum-T-Bigram-Question.csv', r'Sum-T-Bigram-Question-Stem.csv',
             r'Sum-T-Trigram-Question.csv', r'Sum-T-Trigram-Question-Stem.csv']

df_ac_bigram_q = pd.read_csv(data_dir +r'Bigram-Question.csv')
df_ac_bigram_q = df_ac_bigram_q.set_index('AC_Doc_ID')

df_ac_bigram_q_buf = df_ac_bigram_q.iloc[:, (Ngram_count_start_from_question -1):]
df_ac_bigram_q_res = pd.DataFrame({ 'Bigram_sum' : df_ac_bigram_q_buf.sum() })
df_ac_bigram_q_res = pd.concat([df_ac_bigram_q_res, df_ac_bigram_q_buf.transpose()], axis = 1)
df_ac_bigram_q_res = df_ac_bigram_q_res.sort_values('Bigram_sum', ascending=False)
df_ac_bigram_q_res.to_csv(data_dir +test_files[0])

df_ac_bigram_q_buf = df_ac_bigram_q[df_ac_bigram_q['Pre_Col_Name'].isin(['Stem'])]
df_ac_bigram_q_buf = df_ac_bigram_q_buf.iloc[:, (Ngram_count_start_from_question -1):]
df_ac_bigram_q_res = pd.DataFrame({ 'Bigram_sum' : df_ac_bigram_q_buf.sum() })
df_ac_bigram_q_res = pd.concat([df_ac_bigram_q_res, df_ac_bigram_q_buf.transpose()], axis = 1)
df_ac_bigram_q_res = df_ac_bigram_q_res.sort_values('Bigram_sum', ascending=False)
df_ac_bigram_q_res = df_ac_bigram_q_res[df_ac_bigram_q_res['Bigram_sum'] >= 1]
df_ac_bigram_q_res.to_csv(data_dir +test_files[1])

df_ac_trigram_q = pd.read_csv(data_dir +r'Trigram-Question.csv')
df_ac_trigram_q = df_ac_trigram_q.set_index('AC_Doc_ID')

df_ac_trigram_q_buf = df_ac_trigram_q.iloc[:, (Ngram_count_start_from_question -1):]
df_ac_trigram_q_res = pd.DataFrame({ 'Trigram_sum' : df_ac_trigram_q_buf.sum() })
df_ac_trigram_q_res = pd.concat([df_ac_trigram_q_res, df_ac_trigram_q_buf.transpose()], axis = 1)
df_ac_trigram_q_res = df_ac_trigram_q_res.sort_values('Trigram_sum', ascending=False)
df_ac_trigram_q_res.to_csv(data_dir +test_files[2])

df_ac_trigram_q_buf = df_ac_trigram_q[df_ac_trigram_q['Pre_Col_Name'].isin(['Stem'])]
df_ac_trigram_q_buf = df_ac_trigram_q_buf.iloc[:, (Ngram_count_start_from_question -1):]
df_ac_trigram_q_res = pd.DataFrame({ 'Trigram_sum' : df_ac_trigram_q_buf.sum() })
df_ac_trigram_q_res = pd.concat([df_ac_trigram_q_res, df_ac_trigram_q_buf.transpose()], axis = 1)
df_ac_trigram_q_res = df_ac_trigram_q_res.sort_values('Trigram_sum', ascending=False)
df_ac_trigram_q_res = df_ac_trigram_q_res[df_ac_trigram_q_res['Trigram_sum'] >= 1]
df_ac_trigram_q_res.to_csv(data_dir +test_files[3])

from file_cmp_diff_ratio import *

for x in test_files:
    file_cmp_diff_ratio(data_dir + x, orig_dir + x)
