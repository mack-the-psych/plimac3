################################################################################
# This module calculates the PMI distribution of item stem and the options. 
# Note that this module does not consider the count of n-gram per stem/option.
# This means that the PMI of each n-gram is equally weighted for the calculation
# of the distribution no matter how many times the n-gram appeared in the stem/
# option.
# Parameters df_ac_ngram_q: input pandas.DataFrame of n-grams, it should have, 
#                     at least, n-gram count columns with the 'AC_Doc_ID's
#                     as the index of the DataFrame
#            ngram_clm_start: integer column number (starting from zero) 
#                             specifying the starting point of n-gram
#                             count columns in the question DataFrame, from 
#                             the point to the end, all the columns should be 
#                             the n-gram count columns
#            df_ac_pmi: pandas.DataFrame of the PMI value of each term
#            gram = 'bigram': specify bigram or trigram
#            decimal_places = None: specify the decimal places to round at
# Returns Result: pandas.DataFrame reporting each 'AC_Doc_ID's PMI stats
################################################################################
def ac_bi_trigram_pmi_distribution(df_ac_ngram_q, ngram_clm_start, df_ac_pmi, 
                      gram = 'bigram', decimal_places = None):
    import pandas as pd
    import numpy as np

    df_ac_buf = df_ac_ngram_q[:]
    df_ac_buf_ngram = df_ac_buf.iloc[:, ngram_clm_start:]

    df_ac_buf_ngram_sum = pd.DataFrame({ 'Ngram_sum' : df_ac_buf_ngram.sum(axis = 1) })
    df_ac_buf_ngram_sum = df_ac_buf_ngram_sum.dropna()

    df_ac_buf_ngram = pd.concat([df_ac_buf_ngram_sum, df_ac_buf_ngram], axis=1, join_axes=[df_ac_buf_ngram_sum.index])
    df_ac_buf_ngram = df_ac_buf_ngram.drop('Ngram_sum', axis=1)

    if gram == 'bigram':
        pmi_ngram = list(df_ac_pmi['Bigram'])
    else:
        pmi_ngram = list(df_ac_pmi['Trigram'])
    
    pmi_dic = {}

    for i, x in enumerate(pmi_ngram):
        pmi_dic[x] = df_ac_pmi.at[df_ac_pmi.index[i], 'PMI']

    t = df_ac_buf_ngram.shape
    clm_lgth = t[1]
    ac_ngram_q_buf_columns = df_ac_buf_ngram.columns

    #df_ac_pmi_diagonal = pd.DataFrame(np.empty((clm_lgth, clm_lgth),
    #    dtype=np.float64), ac_ngram_q_buf_columns, ac_ngram_q_buf_columns)
    df_ac_pmi_diagonal = pd.DataFrame(np.zeros((clm_lgth, clm_lgth),
        dtype=np.float64), ac_ngram_q_buf_columns, ac_ngram_q_buf_columns)

    for i, x in enumerate(ac_ngram_q_buf_columns):
        if x in pmi_dic:
            df_ac_pmi_diagonal.iloc[i, i] = float(pmi_dic[x])
        else:
            df_ac_pmi_diagonal.iloc[i, i] = float(0.0)

    #df_ac_pmi_diagonal = df_ac_pmi_diagonal.fillna(0.0)

    # the count of n-gram per stem/option is not considered
    df_ac_buf_ngram_no_weight = df_ac_buf_ngram / df_ac_buf_ngram
    df_ac_buf_ngram_no_weight_fillzero = df_ac_buf_ngram_no_weight.fillna(0.0)

    df_ac_ngram_q_pmi_mtx = df_ac_buf_ngram_no_weight_fillzero.dot(df_ac_pmi_diagonal)

    # PMI matrix to be with N/A cells
    df_ac_ngram_q_pmi_mtx = df_ac_ngram_q_pmi_mtx * df_ac_buf_ngram_no_weight

    if gram == 'bigram':
        if decimal_places != None:
            df_ac_ngram_q_pmi_mean = pd.DataFrame({ 'PMI_Bigram_Mean' : df_ac_ngram_q_pmi_mtx.mean(axis=1).round(decimal_places) })
            df_ac_ngram_q_pmi_sd = pd.DataFrame({ 'PMI_Bigram_SD' : df_ac_ngram_q_pmi_mtx.std(axis=1).round(decimal_places) })
            df_ac_ngram_q_pmi_max = pd.DataFrame({ 'PMI_Bigram_Max' : df_ac_ngram_q_pmi_mtx.max(axis=1).round(decimal_places) })
            df_ac_ngram_q_pmi_min = pd.DataFrame({ 'PMI_Bigram_Min' : df_ac_ngram_q_pmi_mtx.min(axis=1).round(decimal_places) })
        else:
            df_ac_ngram_q_pmi_mean = pd.DataFrame({ 'PMI_Bigram_Mean' : df_ac_ngram_q_pmi_mtx.mean(axis=1) })
            df_ac_ngram_q_pmi_sd = pd.DataFrame({ 'PMI_Bigram_SD' : df_ac_ngram_q_pmi_mtx.std(axis=1) })
            df_ac_ngram_q_pmi_max = pd.DataFrame({ 'PMI_Bigram_Max' : df_ac_ngram_q_pmi_mtx.max(axis=1) })
            df_ac_ngram_q_pmi_min = pd.DataFrame({ 'PMI_Bigram_Min' : df_ac_ngram_q_pmi_mtx.min(axis=1) })

        df_ac_ngram_q_pmi_mean['PMI_Bigram_SD'] = df_ac_ngram_q_pmi_sd['PMI_Bigram_SD']
        df_ac_ngram_q_pmi_mean['PMI_Bigram_Max'] = df_ac_ngram_q_pmi_max['PMI_Bigram_Max']
        df_ac_ngram_q_pmi_mean['PMI_Bigram_Min'] = df_ac_ngram_q_pmi_min['PMI_Bigram_Min']
    else:
        if decimal_places != None:
            df_ac_ngram_q_pmi_mean = pd.DataFrame({ 'PMI_Trigram_Mean' : df_ac_ngram_q_pmi_mtx.mean(axis=1).round(decimal_places) })
            df_ac_ngram_q_pmi_sd = pd.DataFrame({ 'PMI_Trigram_SD' : df_ac_ngram_q_pmi_mtx.std(axis=1).round(decimal_places) })
            df_ac_ngram_q_pmi_max = pd.DataFrame({ 'PMI_Trigram_Max' : df_ac_ngram_q_pmi_mtx.max(axis=1).round(decimal_places) })
            df_ac_ngram_q_pmi_min = pd.DataFrame({ 'PMI_Trigram_Min' : df_ac_ngram_q_pmi_mtx.min(axis=1).round(decimal_places) })
        else:
            df_ac_ngram_q_pmi_mean = pd.DataFrame({ 'PMI_Trigram_Mean' : df_ac_ngram_q_pmi_mtx.mean(axis=1) })
            df_ac_ngram_q_pmi_sd = pd.DataFrame({ 'PMI_Trigram_SD' : df_ac_ngram_q_pmi_mtx.std(axis=1) })
            df_ac_ngram_q_pmi_max = pd.DataFrame({ 'PMI_Trigram_Max' : df_ac_ngram_q_pmi_mtx.max(axis=1) })
            df_ac_ngram_q_pmi_min = pd.DataFrame({ 'PMI_Trigram_Min' : df_ac_ngram_q_pmi_mtx.min(axis=1) })

        df_ac_ngram_q_pmi_mean['PMI_Trigram_SD'] = df_ac_ngram_q_pmi_sd['PMI_Trigram_SD']
        df_ac_ngram_q_pmi_mean['PMI_Trigram_Max'] = df_ac_ngram_q_pmi_max['PMI_Trigram_Max']
        df_ac_ngram_q_pmi_mean['PMI_Trigram_Min'] = df_ac_ngram_q_pmi_min['PMI_Trigram_Min']

    df_ac_ngram_q_head = df_ac_ngram_q.iloc[:, :ngram_clm_start]
    df_ac_buf_ngram_pim = pd.concat([df_ac_ngram_q_head, df_ac_ngram_q_pmi_mean], axis = 1, join_axes=[df_ac_ngram_q_head.index])

    return df_ac_buf_ngram_pim
