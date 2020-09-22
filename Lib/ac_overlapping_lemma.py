################################################################################
# This module counts overlapping lemmas among an item stem and the options from 
# the input lemma count columns. If the lemma count columns of passage sections  
# are also specified as the other input, the overlapping lemmas with  
# the corresponded item stem or the options are also counted.
# Parameters df_ac_q: input pandas.DataFrame of questions, it should have,  
#                     at least, lemma count columns with the 'AC_Doc_ID's   
#                     as the index of the DataFrame, the question ID column, and
#                     stem/option identifier column, if the DataFrame of 
#                     passages are also specified as the other input, 
#                     the DataFrame of questions should also have corresponded 
#                     passage name and the section columns, the module assumes 
#                     that the stem and options which have the same question 
#                     ID share the same passage name and the section(s)
#            question_id_clm: column name of question IDs which are shared by
#                             the item stem and the options of each question 
#            stem_option_name_clm: column name of stem/option identifier 
#            lemma_start_q: integer column number (starting from zero) 
#                           specifying the starting point of lemma count 
#                           columns in the question DataFrame, from the point 
#                           to the end, all the columns should be the lemma 
#                           count columns
#            stop_words = None: list of lemmas to specify stop words, they 
#                               should all include in the question and passage 
#                               DataFrames
#            passage_name_clm_q = None: column name of the passage names 
#                                       in the question DataFrame
#            passage_sec_clm_q = None: column name of the passage sections 
#                                       in the question DataFrame
#            df_ac_p = None: input pandas.DataFrame of passages, it should have,
#                     at least, lemma count columns, passage name 
#                     and the section columns
#            passage_name_clm_p = None: column name of the passage names 
#                                       in the passage DataFrame
#            passage_sec_clm_p = None: column name of the passage sections 
#                                       in the passage DataFrame
#            lemma_start_p = None: integer column number (starting from zero) 
#                           specifying the starting point of lemma count 
#                           columns in the passage DataFrame, from the point 
#                           to the end, all the columns should be the lemma 
#                           count columns
# Returns Result: pandas.DataFrame as a result of overlapping lemma counts
################################################################################
def ac_overlapping_lemma(df_ac_q, question_id_clm, stem_option_name_clm, 
                         lemma_start_q, stop_words = None,
                         passage_name_clm_q = None, passage_sec_clm_q = None,
                         df_ac_p = None, passage_name_clm_p = None,
                         passage_sec_clm_p = None, lemma_start_p = None):
    import pandas as pd
    import numpy as np

    df_ac_buf = df_ac_q.copy()
    df_ac_id_buf = df_ac_buf[question_id_clm]
    df_ac_id = df_ac_id_buf.drop_duplicates()

    ac_buf_index_name = df_ac_buf.index.name
    ac_buf_index = df_ac_buf.index

    df_ac_buf = df_ac_buf.set_index([question_id_clm, stem_option_name_clm])
    df_ac_buf_lemma = df_ac_buf.iloc[:, (lemma_start_q -2):]

    if stop_words != None:
        df_ac_buf_lemma = df_ac_buf_lemma.drop(stop_words, axis=1)

    if df_ac_p is not None:
        df_ac_buf_p = df_ac_p.copy()
        df_ac_buf_p = df_ac_buf_p.set_index([passage_name_clm_p, passage_sec_clm_p])
        # modified by Makoto.Sano@Mack-the-Psych.com 09/22/2020
        if stop_words != None:
            df_ac_buf_p = df_ac_buf_p.drop(stop_words, axis=1)
        df_ac_buf_p_lemma = df_ac_buf_p.iloc[:, (lemma_start_p -2):]

        # modified by Makoto.Sano@Mack-the-Psych.com 09/22/2020
        # In order to avoid overhead of the appending operation for each row,
        # the passage name and passage section name are compounded as a temporal index name
        df_ac_buf_p_lemma[question_id_clm] = [x[0] + ';' + x[1] for x in df_ac_buf_p_lemma.index]
        df_ac_buf_p_lemma[stem_option_name_clm] = 'Passage'
        df_ac_buf_p_lemma = df_ac_buf_p_lemma.set_index([question_id_clm, stem_option_name_clm])

        row_lgth = df_ac_buf_lemma.shape[0]
        df_ac_buf_q_p_lemma = df_ac_buf_lemma.append(df_ac_buf_p_lemma)
        df_ac_buf_lemma = df_ac_buf_q_p_lemma.iloc[:row_lgth, :]
        df_ac_buf_p_lemma = df_ac_buf_q_p_lemma.iloc[row_lgth:, :]
        
    df_res = pd.DataFrame()

    for x in df_ac_id:
        print('Question:' + str(x))

        if df_ac_p is not None:
            df_q_x = df_ac_buf.xs(x)
            passage_name = df_q_x[passage_name_clm_q][0]
            passage_sections = (df_q_x[passage_sec_clm_q][0]).split(';')            

            print('Passage:' + passage_name)

            # modified by Makoto.Sano@Mack-the-Psych.com 09/22/2020
            # df_p_x = df_ac_buf_p.xs(passage_name)
            # df_p_x = df_p_x.loc[passage_sections]
            # df_ac_buf_p_lemma_x = df_p_x.iloc[:, (lemma_start_p -2):]

            # modified by Makoto.Sano@Mack-the-Psych.com 09/22/2020
            # In order to avoid overhead of the appending operation for each row,
            # the passage name and passage section name are compounded as a temporal index name
            # df_ac_buf_p_lemma_x = df_ac_buf_p_lemma.xs(passage_name)
            # df_ac_buf_p_lemma_x = df_ac_buf_p_lemma_x.loc[passage_sections]
            df_ac_buf_p_lemma_x = df_ac_buf_p_lemma[[x[0].startswith(passage_name) for x in df_ac_buf_p_lemma.index]]
            df_ac_buf_p_lemma_x = df_ac_buf_p_lemma_x[[x[0].endswith(tuple(passage_sections)) for x in df_ac_buf_p_lemma_x.index]]
            
            # modified by Makoto.Sano@Mack-the-Psych.com 09/22/2020
            # if stop_words != None:
            #     df_ac_buf_p_lemma_x = df_ac_buf_p_lemma_x.drop(stop_words, axis=1)
            
            df_ac_buf_p_lemma_x_sum = pd.DataFrame({ 'Passage' : df_ac_buf_p_lemma_x.sum() })
    
            df_ac_buf_lemma_x = (df_ac_buf_p_lemma_x_sum.transpose()).append(df_ac_buf_lemma.xs(x))
            index_arr = df_ac_buf_lemma_x.index.values
            index_arr = np.append(index_arr[1:], index_arr[0])
            df_ac_buf_lemma_x = df_ac_buf_lemma_x.reindex(index_arr)
            
            df_ac_buf_lemma_x.index.name = stem_option_name_clm
            df_ac_overlap_doc = ac_overlapping_terms(df_ac_buf_lemma_x)
            df_ac_overlap_doc = df_ac_overlap_doc.drop('Passage', axis=0)
        else:
            df_ac_overlap_doc = ac_overlapping_terms(df_ac_buf_lemma.xs(x))
       
        df_ac_overlap_doc = df_ac_overlap_doc.reset_index()
        df_doc = pd.DataFrame({ question_id_clm : np.array([x] *
                len(df_ac_overlap_doc)) })
        df_ac_overlap_doc[question_id_clm] = df_doc[question_id_clm]
        df_res = df_res.append(df_ac_overlap_doc, ignore_index=True)

    df_doc_id = pd.DataFrame({ ac_buf_index_name : ac_buf_index })
    df_res[ac_buf_index_name] = df_doc_id[ac_buf_index_name]
    df_res = df_res.set_index(ac_buf_index_name)
    
    return df_res

################################################################################
# This module counts overlapping lemmas among the all input records
# Parameters df_ac_q: input pandas.DataFrame it should only have lemma count 
#                     columns with an index of the DataFrame
# Returns Result: pandas.DataFrame as a result of overlapping lemma counts
################################################################################
def ac_overlapping_terms(df_doc_term_matrix):
    import pandas as pd
    import numpy as np

    t = df_doc_term_matrix.shape
    row_lgth = t[0]
    col_lgth = t[1]
    doc_term_matrix_clm_count = []
    doc_term_matrix_clm_terms = []
    doc_term_matrix_index = df_doc_term_matrix.index
    doc_term_matrix_clms = df_doc_term_matrix.columns

    for x in doc_term_matrix_index:
        s = 'Count_' + x
        doc_term_matrix_clm_count.append(s)  

    for x in doc_term_matrix_index:
        s = 'Terms_' + x 
        doc_term_matrix_clm_terms.append(s)  

#    df_overlapping_matrix = pd.DataFrame(np.empty((row_lgth, row_lgth * 2),
#                    dtype=object), doc_term_matrix_index,
#                    doc_term_matrix_clm_count + doc_term_matrix_clm_terms)

    df_overlapping_count_matrix = pd.DataFrame(np.empty((row_lgth, row_lgth),
                    dtype=np.int64), doc_term_matrix_index,
                    doc_term_matrix_clm_count)

    df_overlapping_term_matrix = pd.DataFrame(np.empty((row_lgth, row_lgth),
                    dtype=object), doc_term_matrix_index,
                    doc_term_matrix_clm_terms)

    # modified by Makoto.Sano@Mack-the-Psych.com 09/20/2020
    '''
    df_overlapping_matrix = pd.concat([df_overlapping_count_matrix, df_overlapping_term_matrix], axis=1)

    for k, z in enumerate(doc_term_matrix_index):
        for i, x in enumerate(doc_term_matrix_clm_count):
            if k == i:
                #df_overlapping_matrix.iloc[k, i] = ''
                df_overlapping_matrix.iloc[k, i] = np.nan
            else:
                df_overlapping_matrix.iloc[k, i] = 0
                df_overlapping_matrix.iloc[k, i + len(doc_term_matrix_clm_count)] = ''
                for j, y in enumerate(df_doc_term_matrix.iloc[i, :]):
                    if y > 0:
                        if df_doc_term_matrix.iloc[k, j] > 0:
                            df_overlapping_matrix.iloc[k, i] += 1
                            s = df_overlapping_matrix.iloc[k, i + len(doc_term_matrix_clm_count)]
                            if s == '':
                                s = doc_term_matrix_clms[j]
                            else:
                                s = ';'.join([s, doc_term_matrix_clms[j]])
                            df_overlapping_matrix.iloc[k, i + len(doc_term_matrix_clm_count)] = s
    '''
    for k, z in enumerate(doc_term_matrix_index):
        for i, x in enumerate(doc_term_matrix_clm_count):
            if k == i:
                df_overlapping_count_matrix.iloc[k, i] = np.nan
            else:
                se_multiply = df_doc_term_matrix.iloc[k] * df_doc_term_matrix.iloc[i]
                se_match = se_multiply / se_multiply
                df_overlapping_count_matrix.iloc[k, i] = int(se_match.sum())

                se_match.index = df_doc_term_matrix.columns
                s = ';'.join(se_match[se_match > 0].index)
                df_overlapping_term_matrix.iloc[k, i] = s

    df_overlapping_matrix = pd.concat([df_overlapping_count_matrix, df_overlapping_term_matrix], axis=1)

    return df_overlapping_matrix
