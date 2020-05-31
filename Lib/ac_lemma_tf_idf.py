################################################################################
# This module calculates TF-IDF from the input lemma count columns of the input
# pandas.DataFrame. The module recognizes each input record as a unit of 
# assessment content (i.e. a single passage section, an item stem, 
# or an item option).
# Parameters df_ac: input pandas.DataFrame of assessment content, it should 
#                     have,at least, lemma count columns with the 'AC_Doc_ID's   
#                     as the index of the DataFrame.
#            lemma_start: integer column number (starting from zero) 
#                           specifying the starting point of lemma count 
#                           columns in the DataFrame, from the point to the end,
#                           all the columns should be the lemma count columns
# Returns Result: pandas.DataFrame including the original columns of the input 
#                 DataFrame except lemma count columns plus TF-IDF calculation 
#                 results
################################################################################
def ac_lemma_tf_idf(df_ac, lemma_start):
    import pandas as pd
    import math

    df_ac_buf = df_ac.iloc[:, lemma_start:]
    df_ac_buf_head = df_ac.iloc[:, :lemma_start]
    df_ac_doc_sum = pd.DataFrame({ 'Doc_sum' : df_ac_buf.sum(axis=1) })

    doc_len = len(df_ac_buf)
    df_ac_tf_idf = df_ac_buf.copy()
    df_ac_df_buf = df_ac_buf.copy()
    doc_term_matrix_clms = df_ac_buf.columns
    term_len = len(doc_term_matrix_clms)

    for j in range(doc_len):
        print('DF for Doc : ' + str(df_ac_df_buf.index[j]))
        for i in range (term_len):
            if df_ac_df_buf.iloc[j, i] >= 1: df_ac_df_buf.iloc[j, i] = 1

    df_res_df = pd.concat([df_ac_buf_head, df_ac_df_buf], axis=1)

    df_ac_df_res = pd.DataFrame({ 'Doc_frq' : df_ac_df_buf.sum() })

    for i in range (term_len):
        idf = math.log(doc_len / df_ac_df_res.iloc[i, 0])
        print('Term (' + doc_term_matrix_clms[i] + ':' + str(df_ac_df_res.iloc[i, 0]) + ') IDF: ' + str(idf))
        for j in range(doc_len):
            tf = df_ac_buf.iloc[j, i] / df_ac_doc_sum.iloc[j, 0]
            df_ac_tf_idf.iloc[j, i] = tf * idf

    df_res_tf_idf = pd.concat([df_ac_buf_head, df_ac_tf_idf], axis=1)

    return df_res_tf_idf, df_res_df
