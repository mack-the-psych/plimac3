import pandas as pd
import filecmp

from ac_overlapping_lemma import *
from ac_overlapping_synset_lemma import *

data_dir = r'../../Data/En/'
orig_dir = r'./orig_data/'

stop_words = [',', '.', '?', 'be', 'a', 'and', 'of', 'to', 'the', 
                            'in', 'on', "'s", "''", '``']

stop_words_syn = [',', '.', '?', 'be', 'a', 'and', 'of', 'to', 'the', 
                            'in', 'on', "'s", '``']

Lemma_count_start_from_question = 23
synset_count_start_from_question = Lemma_count_start_from_question
Lemma_count_start_from_passage = 5

test_files= [r'Overlapping-Lemma.csv', r'Overlapping-Synset-Lemma.csv']

df_ac_lemma_q = pd.read_csv(data_dir + r'Lemma-Question.csv')
df_ac_lemma_q = df_ac_lemma_q.set_index('AC_Doc_ID')

df_ac_lemma_p = pd.read_csv(data_dir + r'Lemma-Passage.csv')
df_ac_lemma_p = df_ac_lemma_p.set_index('AC_Doc_ID')

df_ac_overlapping_lemma = ac_overlapping_lemma(df_ac_lemma_q, 'Question#', 'Pre_Col_Name',
                            Lemma_count_start_from_question - 1, stop_words,
                            'Passage_Name', 'Reference_Passage_Section',
                            df_ac_lemma_p, 'Passage_Name',
                            'Passage_Section', Lemma_count_start_from_passage -1)

df_ac_overlapping_lemma.to_csv(data_dir + test_files[0])

df_ac_synset_q = pd.read_csv(data_dir + r'Synset-Question.csv')
df_ac_synset_q = df_ac_synset_q.set_index('AC_Doc_ID')

df_ac_overlapping_syn_lemma = ac_overlapping_synset_lemma(df_ac_lemma_q, 'Question#', 'Pre_Col_Name',
                            Lemma_count_start_from_question - 1, df_ac_synset_q,
                            synset_count_start_from_question - 1, stop_words_syn,
                            'Passage_Name', 'Reference_Passage_Section',
                            df_ac_lemma_p, 'Passage_Name',
                            'Passage_Section', Lemma_count_start_from_passage -1)

df_ac_overlapping_syn_lemma.to_csv(data_dir + test_files[1])

from file_cmp_diff_ratio import *

for x in test_files:
    file_cmp_diff_ratio(data_dir + x, orig_dir + x)
