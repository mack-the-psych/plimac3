import pandas as pd
import filecmp

data_dir = r'../../Data/En/'
orig_dir = r'./orig_data/'

from ac_aggregate_plim import *

Stop_words_POS = [',', '.', "''", '``', 'DT']
Keep_specific_columns_POS = ['Question#', 'Passage_Name',
                                      'Reference_Passage_Section', 'Key',
                                      'Difficulty', 'Proportion_Correct', 'Avg_Score', 'Year', 
                                      'Description', 'Pre_Col_Name',
                                      'Content', 'Aspects of Reading (1992-2007)', 'Cognitive Target (2009 and on)']
Include_specific_lemma_count = ['author', 'passage']

POS_count_start_from_passage = 5
POS_count_start_from_question = 23
Decimal_places = 4
Stem_option_name_clm = 'Pre_Col_Name'
Stem_identifier = 'Stem'
PMI_values_start_from_question = 22

test_file = r'Aggregate_plim.csv'

df_ac_pos_q = pd.read_csv(data_dir + r'POS-Question.csv')
df_ac_pos_q = df_ac_pos_q.set_index('AC_Doc_ID')

df_ac_loc_overlapping_lemma = pd.read_csv(data_dir + r'Loc-Overlapping-Lemma.csv')
df_ac_loc_overlapping_lemma = df_ac_loc_overlapping_lemma.set_index('AC_Doc_ID')
df_ac_loc_overlapping_lemma = df_ac_loc_overlapping_lemma.drop(['Question#', 'Pre_Col_Name'],
                                                       axis=1)

df_ac_loc_overlapping_syn_lemma = pd.read_csv(data_dir + r'Loc-Overlapping-Synset-Lemma.csv')
df_ac_loc_overlapping_syn_lemma = df_ac_loc_overlapping_syn_lemma.set_index('AC_Doc_ID')
df_ac_loc_overlapping_syn_lemma = df_ac_loc_overlapping_syn_lemma.drop(['Question#', 'Pre_Col_Name'],
                                                       axis=1)

df_ac_oanc_lemma_freq_q = pd.read_csv(data_dir + r'Lemma-OANC-Frequency.csv')
df_ac_oanc_lemma_freq_q = df_ac_oanc_lemma_freq_q.set_index('AC_Doc_ID')
df_ac_oanc_lemma_freq_q = df_ac_oanc_lemma_freq_q.drop(['Question#', 'Pre_Col_Name'],
                                                       axis=1)

df_ac_overlapping_nchunk = pd.read_csv(data_dir + r'Overlapping-NChunk.csv')
df_ac_overlapping_nchunk = df_ac_overlapping_nchunk.set_index('AC_Doc_ID')
df_ac_overlapping_nchunk = df_ac_overlapping_nchunk.drop(['Question#', 'Pre_Col_Name'],
                                                       axis=1)

df_ac_lemma_q = pd.read_csv(data_dir + r'Lemma-Question.csv')
df_ac_lemma_q = df_ac_lemma_q.set_index('AC_Doc_ID')

df_ac_pos_p = pd.read_csv(data_dir + r'POS-Passage.csv')
df_ac_pos_p = df_ac_pos_p.set_index('AC_Doc_ID')

df_ac_overlapping_hype_lemma = pd.read_csv(data_dir + r'Overlapping-Hypernyms-Lemma.csv')
df_ac_overlapping_hype_lemma = df_ac_overlapping_hype_lemma.set_index('AC_Doc_ID')
df_ac_overlapping_hype_lemma = df_ac_overlapping_hype_lemma.drop(['Question#', 'Pre_Col_Name'],
                                                       axis=1)

df_ac_overlapping_hypo_lemma = pd.read_csv(data_dir + r'Overlapping-Hyponyms-Lemma.csv')
df_ac_overlapping_hypo_lemma = df_ac_overlapping_hypo_lemma.set_index('AC_Doc_ID')
df_ac_overlapping_hypo_lemma = df_ac_overlapping_hypo_lemma.drop(['Question#', 'Pre_Col_Name'],
                                                       axis=1)

df_ac_bigram_q_pmi = pd.read_csv(data_dir + r'PMI-Distribution-Bigram-Question.csv')
df_ac_bigram_q_pmi = df_ac_bigram_q_pmi.set_index('AC_Doc_ID')
df_ac_bigram_q_pmi = df_ac_bigram_q_pmi.iloc[:, (PMI_values_start_from_question -1):]

df_ac_trigram_q_pmi = pd.read_csv(data_dir + r'PMI-Distribution-Trigram-Question.csv')
df_ac_trigram_q_pmi = df_ac_trigram_q_pmi.set_index('AC_Doc_ID')
df_ac_trigram_q_pmi = df_ac_trigram_q_pmi.iloc[:, (PMI_values_start_from_question -1):]

df_ac_aggregate = ac_aggregate_plim(df_ac_pos_q, (POS_count_start_from_question - 1), 
                          df_ac_loc_overlapping_lemma, df_ac_loc_overlapping_syn_lemma, 
                          df_ac_overlapping_nchunk, df_ac_oanc_lemma_freq_q, Stem_option_name_clm, Stem_identifier,
                          Keep_specific_columns_POS, Stop_words_POS, df_ac_lemma_q, Include_specific_lemma_count,
                          df_ac_pos_p, 'Passage_Name', 'Reference_Passage_Section',
                          'Passage_Name', 'Passage_Section', (POS_count_start_from_passage - 1), Decimal_places,
                          df_ac_overlapping_hype_lemma, df_ac_overlapping_hypo_lemma,
                          df_ac_bigram_pmi_distribution = df_ac_bigram_q_pmi, 
                          df_ac_trigram_pmi_distribution = df_ac_trigram_q_pmi)

df_ac_aggregate.to_csv(data_dir + test_file)

from file_cmp_diff_ratio import *

file_cmp_diff_ratio(data_dir + test_file, orig_dir + test_file) 
