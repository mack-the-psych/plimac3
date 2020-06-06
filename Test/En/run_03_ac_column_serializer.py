import filecmp

from ac_column_serializer import *

data_dir = r'../../Data/En/'
orig_dir = r'./orig_data/'

colnames_ser = ['Stem','A', 'B','C','D']
test_file = r'Serialized-Manual_Edit-ContentMatix-Question-NAEP-G8-Reading-92-13.csv'

df_res = ac_column_serializer(
    data_dir + r'Manual_Edit-ContentMatix-Question-NAEP-G8-Reading-92-13.csv', 'Question#',
    colnames_ser)

df_res.to_csv(data_dir + test_file)

from file_cmp_diff_ratio import *

file_cmp_diff_ratio(data_dir + test_file, orig_dir + test_file)
