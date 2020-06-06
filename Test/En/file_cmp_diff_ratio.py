import filecmp
import difflib

def file_cmp_diff_ratio(file1, file2):
    print('Match test against:', file2, filecmp.cmp(file1, file2))

    with open(file1,'r') as f:
        str1 = f.readlines()
    	
    with open(file2,'r') as f:
        str2 = f.readlines()

    print('Str match ratio:', difflib.SequenceMatcher(None, str1, str2).ratio())
