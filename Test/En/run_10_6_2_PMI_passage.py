import pandas as pd
import numpy as np
import filecmp

data_dir = r'../../Data/En/'
orig_dir = r'./orig_data/'

from ac_term_proportion import *
from ac_bi_trigram_pmi import *

Lemma_count_start_from_passage = 5
Ngram_count_start_from_Passage = Lemma_count_start_from_passage
Decimal_places = 4

test_files= [r'PMI-Sum-T-Bigram-Passage.csv', r'PMI-Sum-T-Trigram-Passage.csv']

df_ac_lemma_p = pd.read_csv(data_dir + r'Lemma-Passage.csv')
df_ac_lemma_p = df_ac_lemma_p.set_index('AC_Doc_ID')
df_ac_sum_t_lemma_q_buf, lemma_sum_total = ac_term_proportion(df_ac_lemma_p, Lemma_count_start_from_passage - 1)

df_ac_bigram_q = pd.read_csv(data_dir + r'Bigram-Passage.csv')
df_ac_bigram_q = df_ac_bigram_q.set_index('AC_Doc_ID')
df_ac_sum_t_bigram_q_buf = ac_bi_trigram_pmi(df_ac_bigram_q, Ngram_count_start_from_Passage - 1,
                                df_ac_sum_t_lemma_q_buf, lemma_sum_total, 'bigram', Decimal_places)
df_ac_sum_t_bigram_q_buf.to_csv(data_dir + test_files[0])

df_ac_trigram_q = pd.read_csv(data_dir + r'Trigram-Passage.csv')
df_ac_trigram_q = df_ac_trigram_q.set_index('AC_Doc_ID')
df_ac_sum_t_trigram_q_buf = ac_bi_trigram_pmi(df_ac_trigram_q, Ngram_count_start_from_Passage - 1,
                                df_ac_sum_t_lemma_q_buf, lemma_sum_total, 'trigram', Decimal_places)
df_ac_sum_t_trigram_q_buf.to_csv(data_dir + test_files[1])

from file_cmp_diff_ratio import *

for x in test_files:
    file_cmp_diff_ratio(data_dir + x, orig_dir + x)
