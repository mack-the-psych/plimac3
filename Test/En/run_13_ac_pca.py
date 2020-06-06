import pandas as pd
import matplotlib.pyplot as plt
import filecmp

import ac_pca as pca

data_dir = r'../../Data/En/'
orig_dir = r'./orig_data/'

test_file = r'PCA.csv'

df_ac_aggregate_item_level = pd.read_csv(data_dir + r'Key-Stem-Passage-Aggregate_plim.csv')

df_ac_buf_pca = df_ac_aggregate_item_level.loc[:,['Count_Passage', 
'Count_Stem', 'Count_s_Passage', 'Count_s_Stem', 'Lemma_Frq_Max', 
'Lemma_Frq_Mean', 'Lemma_Frq_Min', 'Lemma_Frq_SD', 'POS_sum', 
'Passage_Lemma_Frq_Max', 'Passage_Lemma_Frq_Mean', 'Passage_Lemma_Frq_Min', 
'Passage_Lemma_Frq_SD', 'Sum_Count_Options', 'Sum_Count_s_Options', 
'Stem_POS_sum', 'Stem_Count_Passage', 'Stem_Count_s_Passage', 
'Stem_Sum_Count_Options', 'Stem_Sum_Count_s_Options', 'Stem_Lemma_Frq_Max', 
'Stem_Lemma_Frq_Mean', 'Stem_Lemma_Frq_Min', 'Stem_Lemma_Frq_SD', 
'Passage_POS_sum', 'Std_Count_Passage', 'Std_Count_s_Passage', 
'Std_Stem_Count_Passage', 'Std_Stem_Count_s_Passage', 'Std_Stem_POS_sum', 
'Count_nc_Passage', 'Count_nc_Stem', 'Sum_Count_nc_Options', 
'Stem_Count_nc_Passage', 'Stem_Sum_Count_nc_Options', 'Stem_Lemma_Count_author', 
'Stem_Lemma_Count_passage', 'Stem_PMI_Bigram_Mean', 'Stem_PMI_Bigram_SD', 
'Stem_PMI_Bigram_Max', 'Stem_PMI_Bigram_Min', 'Stem_PMI_Trigram_Mean', 
'Stem_PMI_Trigram_SD', 'Stem_PMI_Trigram_Max']]

Feature_value_labels = ['OLP_Number_Ovl_Lemma_w_Passage', 
'OLS_Number_Ovl_Lemma_w_Stem', 'OSP_Number_Ovl_Synonym_w_Passage', 
'OSS_Number_Ovl_Synonym_w_Stem', 'FRQ_Lemma_Frq_Max', 'FRQ_Lemma_Frq_Mean', 
'FRQ_Lemma_Frq_Min', 'FRQ_Lemma_Frq_SD', 'POS_Part_of_speech_Count', 'Passage_FRQ_Lemma_Frq_Max', 
'Passage_FRQ_Lemma_Frq_Mean', 'Passage_FRQ_Lemma_Frq_Min', 'Passage_FRQ_Lemma_Frq_SD', 
'OLO_Number_Ovl_Lemma_w_Distractor_Options', 'OSO_Number_Ovl_Synonym_w_Distractor_Options', 
'Stem_POS_Part_of_speech_Count', 'Stem_OLP_Number_Ovl_Lemma_w_Passage', 
'Stem_OSP_Number_Ovl_Synonym_w_Passage', 'Stem_OLO_Number_Ovl_Lemma_w_All_Options', 
'Stem_OSO_Number_Ovl_Synonym_w_All_Options', 'Stem_FRQ_Lemma_Frq_Max', 'Stem_FRQ_Lemma_Frq_Mean', 
'Stem_FRQ_Lemma_Frq_Min', 'Stem_FRQ_Lemma_Frq_SD', 'Passage_POS_Part_of_speech_Count', 
'sOLP_Std_Number_Ovl_Lemma_w_Passage', 'sOSP_Std_Number_Ovl_Synonym_w_Passage', 
'Stem_sOLP_Std_Number_Ovl_Lemma_w_Passage', 'Stem_sOSP_Std_Number_Ovl_Synonym_w_Passage', 
'Stem_sPOS_Std_Part_of_speech_Count', 'ONCP_Number_Ovl_NChunk_w_Passage', 
'ONCS_Number_Ovl_NChunk_w_Stem', 'ONCO_Number_Ovl_NChunk_w_Distractor_Options', 
'Stem_ONCP_Number_Ovl_NChunk_w_Passage', 'Stem_ONCO_Number_Ovl_NChunk_w_All_Options', 
'Stem_Lemma_author', 'Stem_Lemma_passage', 'Stem_PMI_Bigram_Mean', 'Stem_PMI_Bigram_SD', 
'Stem_PMI_Bigram_Max', 'Stem_PMI_Bigram_Min', 'Stem_PMI_Trigram_Mean', 
'Stem_PMI_Trigram_SD', 'Stem_PMI_Trigram_Max']

df_ac_pca = pca.ac_pca(df_ac_buf_pca, Feature_value_labels)

df_ac_pca.to_csv(data_dir + test_file)

from file_cmp_diff_ratio import *

file_cmp_diff_ratio(data_dir + test_file, orig_dir + test_file) 

ev = df_ac_pca.loc[u'EIGEN_VALUES']
plt.plot(df_ac_pca.columns, ev, label = 'Eigenvalue', color = 'k', marker='o')
plt.xlim([0, len(ev)])
plt.xlabel('Component Number')
plt.ylabel('Eigenvalue')
plt.savefig(data_dir + r'PCA-scree-plot.png')
plt.show()

