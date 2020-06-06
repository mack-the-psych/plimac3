import pandas as pd
import numpy as np
import filecmp

from ac_term_proportion import *
from ac_bi_trigram_pmi import *

data_dir = r'../../Data/En/'
orig_dir = r'./orig_data/'

Lemma_count_start_from_question = 23
Ngram_count_start_from_question = Lemma_count_start_from_question
Decimal_places = 4

test_files= [r'PMI-Sum-T-Bigram-Question.csv', r'PMI-Sum-T-Trigram-Question.csv']

df_ac_lemma_q = pd.read_csv(data_dir + r'Lemma-Question.csv')
df_ac_lemma_q = df_ac_lemma_q.set_index('AC_Doc_ID')
df_ac_sum_t_lemma_q_buf, lemma_sum_total = ac_term_proportion(df_ac_lemma_q, Lemma_count_start_from_question - 1)

df_ac_bigram_q = pd.read_csv(data_dir + r'Bigram-Question.csv')
df_ac_bigram_q = df_ac_bigram_q.set_index('AC_Doc_ID')
df_ac_sum_t_bigram_q_buf = ac_bi_trigram_pmi(df_ac_bigram_q, Ngram_count_start_from_question - 1,
                                df_ac_sum_t_lemma_q_buf, lemma_sum_total, 'bigram', Decimal_places)
df_ac_sum_t_bigram_q_buf.to_csv(data_dir + test_files[0])

df_ac_trigram_q = pd.read_csv(data_dir + r'Trigram-Question.csv')
df_ac_trigram_q = df_ac_trigram_q.set_index('AC_Doc_ID')
df_ac_sum_t_trigram_q_buf = ac_bi_trigram_pmi(df_ac_trigram_q, Ngram_count_start_from_question - 1,
                                df_ac_sum_t_lemma_q_buf, lemma_sum_total, 'trigram', Decimal_places)
df_ac_sum_t_trigram_q_buf.to_csv(data_dir + test_files[1])

from file_cmp_diff_ratio import *

for x in test_files:
    file_cmp_diff_ratio(data_dir + x, orig_dir + x)
