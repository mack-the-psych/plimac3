################################################################################
# This module calculates the proportion of terms (e.g. lemmas) by summing 
# the term counts across the questions and devided by the total number of terms.
# Parameters df_ac_q: input pandas.DataFrame of questions, it should have, 
#                     at least, term (lemma) count columns with the 'AC_Doc_ID's
#                     as the index of the DataFrame
#            lemma_clm_start: integer column number (starting from zero) 
#                             specifying the starting point of term (lemma) 
#                             count columns in the question DataFrame, from 
#                             the point to the end, all the columns should be 
#                             the term count columns
# Returns Result: pandas.DataFrame as the proportion of terms and
#                 the total number of terms
################################################################################
def ac_term_proportion(df_ac_q, lemma_clm_start):
    import pandas as pd
    import numpy as np

    df_ac_buf = df_ac_q[:]
    df_ac_buf_lemma = df_ac_buf.iloc[:, lemma_clm_start:]
    df_ac_lemma_q_res = pd.DataFrame({ 'Lemma_sum' : df_ac_buf_lemma.sum() })

    #Updated 3/5/2017 mack.sano@gmail.com
    pd_ver = list(map(int, pd.__version__.split('.')))
    if (pd_ver[0] > 0) or (pd_ver[1] >= 18): #the version needs to be confirmed (Updated 9/26/2017 mack.sano@gmail.com)
        lemma_sum_total = df_ac_lemma_q_res.iloc[:,0].sum()
    else:
        lemma_sum_total = df_ac_lemma_q_res.iloc[:,0].sum(axis=1)

    df_ac_lemma_q_res.index.name = 'Lemma'

    t = df_ac_lemma_q_res.shape
    row_lgth = t[0]
    ac_sum_t_lemma_q_buf_index = df_ac_lemma_q_res.index

    df_ac_sum_t_lemma_q_p_x = pd.DataFrame(np.empty((row_lgth, 1),
                    dtype=np.float64), ac_sum_t_lemma_q_buf_index,
                    ['p_x'])

    for i, x in enumerate(ac_sum_t_lemma_q_buf_index):
        df_ac_sum_t_lemma_q_p_x.iloc[i, 0] = (df_ac_lemma_q_res.iloc[i, 0] / 
            lemma_sum_total)

    df_ac_lemma_q_res['p_x'] = df_ac_sum_t_lemma_q_p_x['p_x']

    return df_ac_lemma_q_res, lemma_sum_total
