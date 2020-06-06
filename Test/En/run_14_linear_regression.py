import pandas as pd
import statsmodels.api as sm
import filecmp

data_dir = r'../../Data/En/'
orig_dir = r'./orig_data/'

test_file = r'Linear_regression.txt'

df_ac_aggregate_item_level = pd.read_csv(data_dir + r'Key-Stem-Passage-Aggregate_plim.csv')

df_ac_buf_ols = df_ac_aggregate_item_level.loc[:,['Avg_Score', 'Lemma_Frq_Max',
'Lemma_Frq_SD', 'POS_sum', 'Passage_Lemma_Frq_Max','Sum_Count_s_Options',
'Stem_Count_Passage', 'Stem_Sum_Count_Options','Stem_Lemma_Frq_Mean', 
'Stem_Lemma_Frq_Min', 'Stem_Lemma_Frq_SD', 'Passage_POS_sum', 
'Stem_Lemma_Count_author', 'Count_hype_Stem', 'Count_hypo_Stem', 
'Stem_Count_hypo_Passage', 'Stem_Sum_Count_hype_Options', 'Stem_Sum_Count_hypo_Options'
]]

df_ac_buf_ols.columns = ['Avg_Score',
'FRQ_Lemma_Frq_Max', 'FRQ_Lemma_Frq_SD', 'POS_Part_of_speech_Count', 
'Passage_FRQ_Lemma_Frq_Max', 'OSO_Number_Ovl_Synonym_w_Distractor_Options', 
'Stem_OLP_Number_Ovl_Lemma_w_Passage', 'Stem_OLO_Number_Ovl_Lemma_w_All_Options', 
'Stem_FRQ_Lemma_Frq_Mean', 'Stem_FRQ_Lemma_Frq_Min', 'Stem_FRQ_Lemma_Frq_SD', 
'Passage_POS_Part_of_speech_Count', 'Stem_Lemma_author',
'Count_hype_Stem', 'Count_hypo_Stem', 'Stem_Count_hypo_Passage', 
'Stem_Sum_Count_hype_Options', 'Stem_Sum_Count_hypo_Options'
]

x_clms = [
'FRQ_Lemma_Frq_Max', 'FRQ_Lemma_Frq_SD', 'POS_Part_of_speech_Count', 
'Passage_FRQ_Lemma_Frq_Max', 'OSO_Number_Ovl_Synonym_w_Distractor_Options', 
'Stem_OLP_Number_Ovl_Lemma_w_Passage', 'Stem_OLO_Number_Ovl_Lemma_w_All_Options', 
'Stem_FRQ_Lemma_Frq_Mean', 'Stem_FRQ_Lemma_Frq_Min', 'Stem_FRQ_Lemma_Frq_SD', 
'Passage_POS_Part_of_speech_Count', 'Stem_Lemma_author'
]

mod = sm.OLS(df_ac_buf_ols['Avg_Score'], sm.add_constant(df_ac_buf_ols[x_clms]))
res = mod.fit()

print(res.summary())

import sys

old_stdout = sys.stdout
fo = open(data_dir + test_file, 'w')
sys.stdout = fo

print(res.summary())

sys.stdout = old_stdout
fo.close()

from file_cmp_diff_ratio import *

file_cmp_diff_ratio(data_dir + test_file, orig_dir + test_file) 
