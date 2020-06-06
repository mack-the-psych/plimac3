import pandas as pd
import filecmp

from ac_overlapping_lemma import *

data_dir = r'../../Data/En/'
orig_dir = r'./orig_data/'

NChunk_count_start_from_question = 23
NChunk_count_start_from_passage = 5

test_file = r'Overlapping-NChunk.csv'

df_ac_nchunk_q = pd.read_csv(data_dir +r'Parsed-Question.csv')
df_ac_nchunk_q = df_ac_nchunk_q.set_index('AC_Doc_ID')

df_ac_nchunk_p = pd.read_csv(data_dir +r'Parsed-Passage.csv')
df_ac_nchunk_p = df_ac_nchunk_p.set_index('AC_Doc_ID')

df_ac_overlapping_nchunk = ac_overlapping_lemma(df_ac_nchunk_q, 'Question#', 'Pre_Col_Name',
                            NChunk_count_start_from_question - 1, None,
                            'Passage_Name', 'Reference_Passage_Section',
                            df_ac_nchunk_p, 'Passage_Name',
                            'Passage_Section', NChunk_count_start_from_passage -1)

column_list = []
for x in df_ac_overlapping_nchunk.columns:
    x = x.replace('Count_', 'Count_nc_')
    x = x.replace('Terms_', 'Terms_nc_')
    #x = x + '_nc'
    column_list = column_list + [x]
df_ac_overlapping_nchunk.columns = column_list

df_ac_overlapping_nchunk.to_csv(data_dir +test_file)

from file_cmp_diff_ratio import *

file_cmp_diff_ratio(data_dir + test_file, orig_dir + test_file)
