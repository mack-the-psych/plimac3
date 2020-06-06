import pandas as pd
import filecmp

import ac_treepredict_by_variance as treepredict
import ac_drawtree_by_difficulty as drawtree

data_dir = r'../../Data/En/'
orig_dir = r'./orig_data/'

test_file = r'Prune-printtree-res.txt'

df_ac_aggregate_item_level = pd.read_csv(data_dir + r'Key-Stem-Passage-Aggregate_plim.csv')

df_ac_buf_tree = df_ac_aggregate_item_level.loc[:,['Avg_Score', 'Count_Passage', 
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
'Stem_Lemma_Count_passage',
'Count_hype_Stem', 'Count_hypo_Stem', 'Stem_Count_hypo_Passage', 
'Stem_Sum_Count_hype_Options', 'Stem_Sum_Count_hypo_Options'
]]

res_column = 'Avg_Score'
data_for_tree_columns = ['OLP_Number_Ovl_Lemma_w_Passage', 
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
'Stem_Lemma_author', 'Stem_Lemma_passage',
'Count_hype_Stem', 'Count_hypo_Stem', 'Stem_Count_hypo_Passage', 
'Stem_Sum_Count_hype_Options', 'Stem_Sum_Count_hypo_Options'
]

df_ac_buf_tree.columns = [res_column] + data_for_tree_columns

tree_data, ac_buf_columns = treepredict.data_for_treebuild(df_ac_buf_tree, 
                                          data_for_tree_columns, res_column)

tree = treepredict.buildtree(tree_data, ac_buf_columns)

treepredict.prune(tree, 30.0)

deviance_dic = {}
treepredict.deviance_by_recursive_call(tree, deviance_dic)
treepredict.finalize_deviance(deviance_dic)

treepredict.printtree(tree)
treepredict.print_r2_by_recursive_call(tree, deviance_dic)

drawtree.drawtree(tree, data_dir + r'Prune-treeview.png', 
        263, 282, deviance_dic, 4, 3)

import sys

old_stdout = sys.stdout
fo = open(data_dir + test_file, 'w')
sys.stdout = fo

treepredict.printtree(tree)
treepredict.print_r2_by_recursive_call(tree, deviance_dic)

sys.stdout = old_stdout
fo.close()

from file_cmp_diff_ratio import *

file_cmp_diff_ratio(data_dir + test_file, orig_dir + test_file) 
