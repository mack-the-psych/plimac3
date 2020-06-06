import pandas as pd
import shelve
import filecmp

from ac_oanc_lemma_frequency import *

oanc_shelve = r'../../Resource/OANC/ANC-all-lemma-04262014.db'
oanc_lemma = shelve.open(oanc_shelve, flag='r')

data_dir = r'../../Data/En/'
orig_dir = r'./orig_data/'

test_file = r'Lemma-OANC-Frequency.csv'

stop_words = [',', '.', '?', 'be', 'a', 'and', 'of', 'to', 'the', 
                            'in', 'on', "'s", "''", '``']

Lemma_count_start_from_question = 23
Lemma_count_start_from_passage = 5
Unknown_word_len_min = 3
Decimal_places = 4

df_ac_lemma_q = pd.read_csv(data_dir + r'Lemma-Question.csv')
df_ac_lemma_q = df_ac_lemma_q.set_index('AC_Doc_ID')

df_ac_lemma_p = pd.read_csv(data_dir + r'Lemma-Passage.csv')
df_ac_lemma_p = df_ac_lemma_p.set_index('AC_Doc_ID')

df_ac_oanc_lemma_freq_q = ac_oanc_lemma_frequency(df_ac_lemma_q, 
                            'Question#', 'Pre_Col_Name', Lemma_count_start_from_question - 1, 
                            oanc_lemma, stop_words, Unknown_word_len_min,
                            'Passage_Name', 'Reference_Passage_Section',
                            df_ac_lemma_p, 'Passage_Name',
                            'Passage_Section', Lemma_count_start_from_passage - 1,
                            Decimal_places)

df_ac_oanc_lemma_freq_q.to_csv(data_dir + test_file)

oanc_lemma.close()

from file_cmp_diff_ratio import *

file_cmp_diff_ratio(data_dir + test_file, orig_dir + test_file)
