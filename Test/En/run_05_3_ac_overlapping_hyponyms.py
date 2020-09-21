import pandas as pd
import filecmp

from ac_overlapping_synset_lemma import *

data_dir = r'../../Data/En/'
orig_dir = r'./orig_data/'

test_file = r'Overlapping-Hyponyms-Lemma.csv'

Lemma_count_start_from_question = 23
hyponyms_count_start_from_question = Lemma_count_start_from_question
Lemma_count_start_from_passage = 5

df_ac_lemma_q = pd.read_csv(data_dir + r'Lemma-Question.csv')
df_ac_lemma_q = df_ac_lemma_q.set_index('AC_Doc_ID')

df_ac_lemma_p = pd.read_csv(data_dir + r'Lemma-Passage.csv')
df_ac_lemma_p = df_ac_lemma_p.set_index('AC_Doc_ID')

df_ac_hyponyms_q = pd.read_csv(data_dir + r'Hyponyms-Question.csv')
df_ac_hyponyms_q = df_ac_hyponyms_q.set_index('AC_Doc_ID')

# modified by Makoto.Sano@Mack-the-Psych.com 09/21/2020
df_ac_overlapping_hyp_lemma = ac_overlapping_synset_lemma(df_ac_lemma_q, 'Question#', 'Pre_Col_Name',
                            Lemma_count_start_from_question - 1, df_ac_hyponyms_q,
                            hyponyms_count_start_from_question - 1, None,
                            'Passage_Name', 'Reference_Passage_Section',
                            df_ac_lemma_p, 'Passage_Name',
                            'Passage_Section', Lemma_count_start_from_passage -1, 'hypo')
'''
column_list = []
for x in df_ac_overlapping_hyp_lemma.columns:
    column_list = column_list + [x.replace('_s_', '_hypo_')]
df_ac_overlapping_hyp_lemma.columns = column_list
'''

df_ac_overlapping_hyp_lemma.to_csv(data_dir + test_file)

from file_cmp_diff_ratio import *

file_cmp_diff_ratio(data_dir + test_file, orig_dir + test_file)
