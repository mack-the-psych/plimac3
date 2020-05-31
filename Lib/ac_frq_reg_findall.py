################################################################################
# This module processes the text in the specified column of the input
# pandas.DataFrame to find all phrases by a regular expression. The module 
# recognizes each input record as a unit of assessment content (i.e. a single 
# passage section, an item stem, or an item option) and applies a serial number
# of 'AC_Doc_ID' to the each output record for the following processing.
# Parameters df_ac: input pandas.DataFrame, it should have, at least, one 
#                   column of text assessment content  
#            content_column: column name of text assessment content for find-all
#            reg_exp_key: search key by a regular expression
#            reg_exp_prefix: specify the prefix of result columns
# Returns Result: pandas.DataFrame including the original columns of the input 
#                 DataFrame plus find-all result columns
################################################################################
def ac_frq_reg_findall(df_ac, content_column, reg_exp_key, reg_exp_prefix):
    import pandas as pd
    import numpy as np
    import re

    df_ac_buf = df_ac.copy()
    list_cntnt = list(df_ac_buf[content_column])
    list_cntnt_reg_exp_find = list_cntnt[:]
    list_doc_id = list_cntnt[:]
    list_find_flg = list_cntnt[:]
    #df_reg_exp_find_all = pd.DataFrame()

    for i, x in enumerate(list_cntnt):
        reg_exp_find = []
        reg_exp_find = re.findall(reg_exp_key, x)
        list_find_flg[i] = len(reg_exp_find)

        if list_find_flg[i] == 0:
            str_reg_exp_find = ''
        else:
            str_reg_exp_find = str(reg_exp_find)
        
        list_cntnt_reg_exp_find[i] = str_reg_exp_find
        print(str_reg_exp_find)

        list_doc_id[i] = i

    title_reg_exp_str = reg_exp_prefix + '_Cntnt'
    title_reg_exp_flg = reg_exp_prefix + '_Frq'

    df_doc_id = pd.DataFrame({ 'AC_Doc_ID' : list_doc_id })
    df_reg_flg = pd.DataFrame({ title_reg_exp_flg : list_find_flg })
    df_cntnt_find = pd.DataFrame({ title_reg_exp_str : list_cntnt_reg_exp_find })

    df_ac_buf['AC_Doc_ID'] = df_doc_id['AC_Doc_ID']
    df_ac_buf[title_reg_exp_str] = df_cntnt_find[title_reg_exp_str]
    df_ac_buf[title_reg_exp_flg] = df_reg_flg[title_reg_exp_flg]

    return df_ac_buf.set_index('AC_Doc_ID')
