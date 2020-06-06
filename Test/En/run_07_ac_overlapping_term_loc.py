import pandas as pd
import filecmp

from ac_overlapping_term_loc_passage import *

data_dir = r'../../Data/En/'
orig_dir = r'./orig_data/'

Decimal_places = 4

test_files= [r'Loc-Overlapping-Lemma.csv', r'Loc-Overlapping-Synset-Lemma.csv']

df_ac_overlapping_lemma = pd.read_csv(data_dir + r'Overlapping-Lemma.csv')
df_ac_overlapping_lemma = df_ac_overlapping_lemma.set_index('AC_Doc_ID')

df_ac_lemma_p = pd.read_csv(data_dir + r'Lemma-Passage.csv')
df_ac_lemma_p = df_ac_lemma_p.set_index('AC_Doc_ID')

df_ac_lemma_q = pd.read_csv(data_dir + r'Lemma-Question.csv')
df_ac_lemma_q = df_ac_lemma_q.set_index('AC_Doc_ID')

df_ac_loc_overlapping_lemma = ac_overlapping_term_loc_passage(df_ac_lemma_q, 
                         'Question#', 'Pre_Col_Name', 'Passage_Name', 
                         'Reference_Passage_Section', df_ac_lemma_p, 'Passage_Name',
                         'Passage_Section', 'Cntnt_Lemma',
                         df_ac_overlapping_lemma, 'Terms_Passage', 'Loc_Lemma_Mean', 
                         'Loc_Lemma_SD', 300,
                         Decimal_places)
                         
df_ac_loc_overlapping_lemma.to_csv(data_dir + test_files[0])

df_ac_overlapping_syn_lemma = pd.read_csv(data_dir + r'Overlapping-Synset-Lemma.csv')
df_ac_overlapping_syn_lemma = df_ac_overlapping_syn_lemma.set_index('AC_Doc_ID')

df_ac_loc_overlapping_syn_lemma = ac_overlapping_term_loc_passage(df_ac_lemma_q, 
                         'Question#', 'Pre_Col_Name', 'Passage_Name', 
                         'Reference_Passage_Section', df_ac_lemma_p, 'Passage_Name',
                         'Passage_Section', 'Cntnt_Lemma',
                         df_ac_overlapping_syn_lemma, 'Terms_s_Passage', 'Loc_Synset_Mean', 
                         'Loc_Synset_SD', 300,
                         Decimal_places)
                         
df_ac_loc_overlapping_syn_lemma.to_csv(data_dir + test_files[1])

from file_cmp_diff_ratio import *

for x in test_files:
    file_cmp_diff_ratio(data_dir + x, orig_dir + x)
