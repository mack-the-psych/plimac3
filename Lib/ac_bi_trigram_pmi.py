################################################################################
# This module calculates the PMI of n-grams
# Parameters df_ac_ngram_q: input pandas.DataFrame of n-grams, it should have, 
#                     at least, n-gram count columns with the 'AC_Doc_ID's
#                     as the index of the DataFrame
#            ngram_clm_start: integer column number (starting from zero) 
#                             specifying the starting point of n-gram
#                             count columns in the question DataFrame, from 
#                             the point to the end, all the columns should be 
#                             the n-gram count columns
#            df_ac_p_x: pandas.DataFrame of the proportion of terms
#            lemma_sum_total: the total number of unigram terms
#            gram = 'bigram': specify bigram or trigram
#            decimal_places = None: specify the decimal places to round at
# Returns Result: pandas.DataFrame as the PMI of n-grams
################################################################################
def ac_bi_trigram_pmi(df_ac_ngram_q, ngram_clm_start, df_ac_p_x, 
                      lemma_sum_total, gram = 'bigram', decimal_places = None):
    import pandas as pd
    import numpy as np
    from math import log

    df_ac_buf = df_ac_ngram_q[:]
    df_ac_buf_ngram = df_ac_buf.iloc[:, ngram_clm_start:]

    if gram == 'bigram':
        df_ac_ngram_q_res = pd.DataFrame({ 'Bigram_sum' : df_ac_buf_ngram.sum() })
        df_ac_ngram_q_res.index.name = 'Bigram'
    else:
        df_ac_ngram_q_res = pd.DataFrame({ 'Trigram_sum' : df_ac_buf_ngram.sum() })
        df_ac_ngram_q_res.index.name = 'Trigram'

    t = df_ac_ngram_q_res.shape
    row_lgth = t[0]
    ac_ngram_q_res_index = df_ac_ngram_q_res.index

    #Updated 9/26/2017 mack.sano@gmail.com
    ac_p_x_index = df_ac_p_x.index

    if gram == 'bigram':
        df_ac_sum_t_bigram_q_p_x = pd.DataFrame(np.empty((row_lgth, 3),
                        dtype=np.float64), ac_ngram_q_res_index,
                        ['p_ab', 'p_a_x_p_b', 'PMI'])

        for i, x in enumerate(ac_ngram_q_res_index):
            #Updated 3/7/2017 mack.sano@gmail.com
            if df_ac_ngram_q_res.iloc[i, 0] > 0:
                df_ac_sum_t_bigram_q_p_x.iloc[i, 0] = df_ac_ngram_q_res.iloc[i, 0] / lemma_sum_total
                print('Bigram: ' + x)
                grams = x.split('_')
                #Updated 9/26/2017 mack.sano@gmail.com
                if grams[0] in ac_p_x_index and grams[1] in ac_p_x_index:
                    df_ac_sum_t_bigram_q_p_x.iloc[i, 1] = df_ac_p_x.loc[grams[0], 'p_x'] * df_ac_p_x.loc[grams[1], 'p_x']
                else:
                    df_ac_sum_t_bigram_q_p_x.iloc[i, 1] = df_ac_sum_t_bigram_q_p_x.iloc[i, 0]
                    print('WARNING: ' + 'The unigram(s) of ' + x + ' cannot be found!!')
                
                if decimal_places != None:
                    df_ac_sum_t_bigram_q_p_x.iloc[i, 2] = round(log( df_ac_sum_t_bigram_q_p_x.iloc[i, 0] / df_ac_sum_t_bigram_q_p_x.iloc[i, 1], 2), decimal_places)
                else:
                    df_ac_sum_t_bigram_q_p_x.iloc[i, 2] = log( df_ac_sum_t_bigram_q_p_x.iloc[i, 0] / df_ac_sum_t_bigram_q_p_x.iloc[i, 1], 2)

        df_ac_ngram_q_res['p_ab'] = df_ac_sum_t_bigram_q_p_x['p_ab']
        df_ac_ngram_q_res['p_a_x_p_b'] = df_ac_sum_t_bigram_q_p_x['p_a_x_p_b']
        df_ac_ngram_q_res['PMI'] = df_ac_sum_t_bigram_q_p_x['PMI']

    else:
        df_ac_sum_t_trigram_q_p_x = pd.DataFrame(np.empty((row_lgth, 3),
                        dtype=np.float64), ac_ngram_q_res_index,
                        ['p_ab', 'p_a_x_p_b_x_p_c', 'PMI'])

        for i, x in enumerate(ac_ngram_q_res_index):
            #Updated 3/7/2017 mack.sano@gmail.com
            if df_ac_ngram_q_res.iloc[i, 0] > 0:
                df_ac_sum_t_trigram_q_p_x.iloc[i, 0] = df_ac_ngram_q_res.iloc[i, 0] / lemma_sum_total # / trigram_sum_total
                print('Trigram: ' + x)
                grams = x.split('_')

                #Updated 9/26/2017 mack.sano@gmail.com
                if grams[0] in ac_p_x_index and grams[1] in ac_p_x_index and grams[2] in ac_p_x_index:
                    df_ac_sum_t_trigram_q_p_x.iloc[i, 1] = (df_ac_p_x.loc[grams[0], 'p_x'] * df_ac_p_x.loc[grams[1], 'p_x'] * df_ac_p_x.loc[grams[2], 'p_x'])
                else:
                    df_ac_sum_t_trigram_q_p_x.iloc[i, 1] = df_ac_sum_t_trigram_q_p_x.iloc[i, 0]
                    print('WARNING: ' + 'The unigram(s) of ' + x + ' cannot be found!!')
                    
                if decimal_places != None:
                    df_ac_sum_t_trigram_q_p_x.iloc[i, 2] = round(log( df_ac_sum_t_trigram_q_p_x.iloc[i, 0] / df_ac_sum_t_trigram_q_p_x.iloc[i, 1], 2), decimal_places)
                else:
                    df_ac_sum_t_trigram_q_p_x.iloc[i, 2] = log( df_ac_sum_t_trigram_q_p_x.iloc[i, 0] / df_ac_sum_t_trigram_q_p_x.iloc[i, 1], 2)

        df_ac_ngram_q_res['p_abc'] = df_ac_sum_t_trigram_q_p_x['p_ab']
        df_ac_ngram_q_res['p_a_x_p_b_x_p_c'] = df_ac_sum_t_trigram_q_p_x['p_a_x_p_b_x_p_c']
        df_ac_ngram_q_res['PMI'] = df_ac_sum_t_trigram_q_p_x['PMI']

    return df_ac_ngram_q_res
