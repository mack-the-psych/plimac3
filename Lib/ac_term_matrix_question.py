################################################################################
# This module creates a question by term (e.g. lemma) matrix in summing the term
# counts across the item stem and the options which share the same question ID.
# Parameters df_ac_q: input pandas.DataFrame of questions, it should have, 
#                     at least, term (lemma) count columns with the 'AC_Doc_ID's
#                     as the index of the DataFrame, the question ID column
#            question_id_clm: column name of question IDs which are shared by
#                             the item stem and the options of each question 
#            lemma_clm_start: integer column number (starting from zero) 
#                             specifying the starting point of term (lemma) 
#                             count columns in the question DataFrame, from 
#                             the point to the end, all the columns should be 
#                             the term count columns
#            stop_words = None: list of terms (lemmas) to specify stop words, 
#                               they should all include in the input DataFrames
# Returns Result: pandas.DataFrame as a question by term matrix
################################################################################
def ac_term_matrix_question(df_ac_q, question_id_clm, lemma_clm_start, 
                         stop_words = None,):
    import pandas as pd
    import numpy as np

    df_ac_buf = df_ac_q[:]
    df_ac_id_buf = df_ac_buf[question_id_clm]
    df_ac_id = df_ac_id_buf.drop_duplicates()

    df_ac_buf = df_ac_buf.reset_index()
    df_ac_buf = df_ac_buf.set_index([question_id_clm])
    
    # Bug fix makoto.sano@prometric.com 07/07/2016
    #df_ac_buf_lemma = df_ac_buf.iloc[:, (lemma_clm_start - 1):]
    df_ac_buf_lemma = df_ac_buf.iloc[:, lemma_clm_start:]

    if stop_words != None:
        df_ac_buf_lemma = df_ac_buf_lemma.drop(stop_words, axis=1)

    df_res = pd.DataFrame()

    for x in df_ac_id:
        print('Question:' + str(x))
        df_q_x = df_ac_buf_lemma.xs(x)

        if isinstance(df_q_x, pd.DataFrame):
            df_q_x_sum = pd.DataFrame({ x : df_q_x.sum() })
        else:
            df_q_x_sum = pd.DataFrame({ x : df_q_x })

        df_res = df_res.append(df_q_x_sum.transpose())

    df_res = df_res.fillna(0)
    df_res.index.name = question_id_clm
    
    return df_res

