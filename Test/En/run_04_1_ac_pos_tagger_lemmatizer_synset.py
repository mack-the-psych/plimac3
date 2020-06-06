import pandas as pd
import filecmp

from ac_pos_tagger import ac_pos_tagger
from ac_lemmatizer import ac_lemmatizer
from ac_synset import ac_synset

data_dir = r'../../Data/En/'
orig_dir = r'./orig_data/'

lemma_count_start_from_question = 23
lemma_count_start_from_passage = 5

test_files= [r'POS-Question.csv', r'POS-Passage.csv', r'Lemma-Question.csv',
             r'Lemma-Passage.csv', r'Synset-Question.csv', r'Synset-Passage.csv']

df_ac_q = pd.read_csv(data_dir + r'Serialized-Manual_Edit-ContentMatix-Question-NAEP-G8-Reading-92-13.csv')
df_ac_pos_q = ac_pos_tagger(df_ac_q, 'Content')
df_ac_pos_q.to_csv(data_dir + test_files[0])

df_ac_p = pd.read_csv(data_dir + r'Manual_Edit-ContentMatix-Reading Passage-NAEP-G8-Reading-92-13.csv')
df_ac_pos_p = ac_pos_tagger(df_ac_p, 'Content')
df_ac_pos_p.to_csv(data_dir + test_files[1])

df_ac_lemma_q = ac_lemmatizer(df_ac_q, 'Content')
df_ac_lemma_q.to_csv(data_dir + test_files[2])

df_ac_lemma_p = ac_lemmatizer(df_ac_p, 'Content')
df_ac_lemma_p.to_csv(data_dir + test_files[3])

df_ac_lemma_q_loc = df_ac_lemma_q.iloc[:,0:(lemma_count_start_from_question - 1)]
df_ac_synset_q = ac_synset(df_ac_lemma_q_loc,'Cntnt_Lemma')
df_ac_synset_q = df_ac_synset_q.drop(['Cntnt_Lemma'], axis=1)

df_ac_synset_q.to_csv(data_dir + test_files[4])

df_ac_lemma_p_loc = df_ac_lemma_p.iloc[:,0:(lemma_count_start_from_passage - 1)]
df_ac_synset_p = ac_synset(df_ac_lemma_p_loc,'Cntnt_Lemma')
df_ac_synset_p = df_ac_synset_p.drop(['Cntnt_Lemma'], axis=1)
df_ac_synset_p.to_csv(data_dir + test_files[5])

from file_cmp_diff_ratio import *

for x in test_files:
    file_cmp_diff_ratio(data_dir + x, orig_dir + x)

