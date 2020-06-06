import pandas as pd
import filecmp

data_dir = r'../../Data/En/'
orig_dir = r'./orig_data/'

from ac_aggregate_item_level_plim import *

Include_specific_Stem_lemma_count = ['author', 'passage']
Decimal_places = 4
Key_clm = 'Key'
Stem_option_name_clm = 'Pre_Col_Name'
Stem_identifier = 'Stem'

test_files= [r'Key-Stem-Passage-Aggregate_plim.csv', r'Corr-Key-Stem-Passage-Aggregate_plim.csv', 
             r'Describe-Key-Stem-Passage-Aggregate_plim.csv']

df_ac_aggregate = pd.read_csv(data_dir + r'Aggregate_plim.csv')
df_ac_aggregate = df_ac_aggregate.set_index('AC_Doc_ID')

df_ac_aggregate_item_level = ac_aggregate_item_level_plim(df_ac_aggregate, Key_clm, 
                               Stem_option_name_clm, Stem_identifier, 
                               Include_specific_Stem_lemma_count, Decimal_places)

df_ac_aggregate_item_level.to_csv(data_dir + test_files[0])
(df_ac_aggregate_item_level.corr()).to_csv(data_dir + test_files[1])
(df_ac_aggregate_item_level.describe()).to_csv(data_dir + test_files[2])

from file_cmp_diff_ratio import *

for x in test_files:
    file_cmp_diff_ratio(data_dir + x, orig_dir + x)
