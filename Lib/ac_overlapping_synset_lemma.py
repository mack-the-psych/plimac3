################################################################################
# This module counts overlapping synonyms of the lemmas in an item stem or 
# the options, with the lemmas in the corresponded options or the item stem, 
# from the input synset count columns. If the lemma count columns of passage 
# sections are also specified as the other input, the overlapping lemmas with 
# the synonyms in the corresponded item stem or the options are also counted.
# When the module counts the overlapping, the overlapping with the original 
# lemmas (as the seeds of the synonyms) are excluded from the counting.
# Parameters df_ac_q: input pandas.DataFrame of questions, it should have,  
#                     at least, lemma count columns with the 'AC_Doc_ID's   
#                     as the index of the DataFrame, the question ID column, and
#                     stem/option identifier column, if the DataFrame of 
#                     passages are also specified as the other input, 
#                     the DataFrame of questions should also have corresponded 
#                     passage name and the section columns, the module assumes 
#                     that the stem and options which have the same question 
#                     ID share the same passage name and the section(s)
#            question_id_clm: column name of question IDs in the lemma question 
#                             DataFrame which are shared by the item stem and 
#                             the options of each question 
#            stem_option_name_clm: column name of stem/option identifier  
#                             in the lemma question DataFrame
#            lemma_start_q: integer column number (starting from zero) 
#                           specifying the starting point of lemma count 
#                           columns in the question DataFrame, from the point 
#                           to the end, all the columns should be the lemma 
#                           count columns
#            df_ac_q_syn: input pandas.DataFrame of questions, it should have,  
#                         at least, synset count columns (they should include
#                         all the lemma count columns which are in the lemma 
#                         question DataFrame) with the 'AC_Doc_ID's as 
#                         the index of the DataFrame (they should be completely 
#                         synchronized with the 'AC_Doc_ID's in the lemma 
#                         question DataFrame), the question ID column, and 
#                         stem/option identifier column
#            synset_start_q: integer column number (starting from zero) 
#                           specifying the starting point of synset count 
#                           columns in the question DataFrame, from the point 
#                           to the end, all the columns should be the synset 
#                           count columns
#            stop_words = None: list of lemmas to specify stop words, they 
#                               should all include in the lemma/synset question 
#                               and passage DataFrames
#            passage_name_clm_q = None: column name of the passage names 
#                                       in the lemma question DataFrame
#            passage_sec_clm_q = None: column name of the passage sections 
#                                       in the lemma question DataFrame
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
#            idntfr = 's': identifier of the output variables
# Returns Result: pandas.DataFrame as a result of overlapping synset counts
################################################################################
# add identfir by Makoto.Sano@Mack-the-Psych.com 09/21/2020
def ac_overlapping_synset_lemma(df_ac_q, question_id_clm, stem_option_name_clm, 
                         lemma_start_q, df_ac_q_syn, 
                         synset_start_q, stop_words = None,
                         passage_name_clm_q = None, passage_sec_clm_q = None,
                         df_ac_p = None, passage_name_clm_p = None,
                         passage_sec_clm_p = None, lemma_start_p = None, idntfr = 's'):
    import pandas as pd
    import numpy as np

    df_ac_buf = df_ac_q.copy()
    df_ac_syn_buf = df_ac_q_syn.copy()
    
    df_ac_id_buf = df_ac_buf[question_id_clm]
    df_ac_id = df_ac_id_buf.drop_duplicates()

    ac_buf_index_name = df_ac_buf.index.name
    ac_buf_index = df_ac_buf.index

    df_ac_buf = df_ac_buf.set_index([question_id_clm, stem_option_name_clm])
    df_ac_buf_lemma = df_ac_buf.iloc[:, (lemma_start_q - 2):]

    # Modified by Makoto.Sano@Mack-the-Psych.com on 06/08/2020
    # df_ac_syn_buf = df_ac_syn_buf.set_index([question_id_clm, stem_option_name_clm])
    df_ac_syn_buf.set_index([question_id_clm, stem_option_name_clm], inplace = True)
    df_ac_syn_buf_synset = df_ac_syn_buf.iloc[:, (synset_start_q -2):]

    if stop_words != None:
        df_ac_buf_lemma = df_ac_buf_lemma.drop(stop_words, axis=1)
        # Modified by Makoto.Sano@Mack-the-Psych.com on 06/08/2020        
        # df_ac_syn_buf_synset = df_ac_syn_buf_synset.drop(stop_words, axis=1)
        df_ac_syn_buf_synset.drop(stop_words, axis=1, inplace = True)

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

    # modified by Makoto.Sano@Mack-the-Psych.com on 09/22/2020
    row_lgth_o = df_ac_buf_lemma.shape[0]
    df_ac_syn_buf_synset_lemma = df_ac_buf_lemma.append(df_ac_syn_buf_synset)
    df_ac_buf_lemma = df_ac_syn_buf_synset_lemma.iloc[:row_lgth_o, :]
    df_ac_syn_buf_synset = df_ac_syn_buf_synset_lemma.iloc[row_lgth_o:, :]
    
    df_ac_syn_buf_synset = ac_clear_overlapping_terms_by_doc(df_ac_syn_buf_synset,
                                                    df_ac_buf_lemma)
        
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
            # df_ac_buf_p_lemma_x = df_p_x.iloc[:, (lemma_start_p - 2):]

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
        else:
            df_ac_buf_lemma_x = df_ac_buf_lemma.xs(x)

        df_ac_syn_buf_synset_x = df_ac_syn_buf_synset.xs(x)

        # modified by Makoto.Sano@Mack-the-Psych.com on 09/22/2020
        # t = df_ac_syn_buf_synset_x.shape
        # row_lgth = t[0]
        # row_lgth_o = df_ac_buf_lemma_x.shape[0]

        # The appending operation takes a few second and needs to be optimized
        # 09/20/2020 Makoto.Sano@Mack-the-Psych.com
        # df_ac_syn_buf_synset_lemma_x = df_ac_buf_lemma_x.append(df_ac_syn_buf_synset_x)
        # df_ac_buf_lemma_x = df_ac_syn_buf_synset_lemma_x.iloc[:row_lgth_o, :]
        # df_ac_syn_buf_synset_x = df_ac_syn_buf_synset_lemma_x.iloc[row_lgth_o:, :]
        
        # modified by Makoto.Sano@Mack-the-Psych.com on 09/22/2020
        # df_ac_syn_buf_synset_x = ac_clear_overlapping_terms_by_doc(df_ac_syn_buf_synset_x,
        #                                                 df_ac_buf_lemma_x)

        # modified by Makoto.Sano@Mack-the-Psych.com 09/21/2020
        df_ac_overlap_doc = ac_overlapping_terms_w_outer_matrix(df_ac_syn_buf_synset_x,
                                                                df_ac_buf_lemma_x, idntfr)
        
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
# This module clears the value in the first input matrix if exactly the same 
# column and record of the second matrix also has a value. the module 
# accommodates to exclude the original lemmas (as the seeds of the synonyms) 
# from the overlapping count and it assumes input two matrices has exactly 
# the same sets of columns.
# Parameters df_cleared_matrix: input pandas.DataFrame it should only have 
#                                synset count columns with an index of 
#                                the DataFrame
#            df_overlapping_matrix: input pandas.DataFrame it should only have 
#                             lemma count columns with an index of 
#                             the DataFrame, 
# Returns Result: pandas.DataFrame as a result of overlapping synset counts
################################################################################
def ac_clear_overlapping_terms_by_doc(df_cleared_matrix, df_overlapping_matrix):
    import pandas as pd

    df_ac_buf = df_cleared_matrix.copy()
    cleared_matrix_index = df_cleared_matrix.index

    for i, x in enumerate(cleared_matrix_index):
        for j, y in enumerate(df_cleared_matrix.iloc[i,:]):
            if y > 0:
                if df_overlapping_matrix.iloc[i, j] > 0:
                    df_ac_buf.iloc[i, j] = None

    return df_ac_buf

################################################################################
# This module counts overlapping lemmas in the all first input matrix records 
# with the all outer matrix records, the module assumes input two matrices 
# has exactly the same sets of columns.
# Parameters df_doc_term_matrix: input pandas.DataFrame it should only have 
#                                synset count columns with an index of 
#                                the DataFrame
#            df_outer_matrix: input pandas.DataFrame it should only have 
#                             lemma count columns with an index of 
#                             the DataFrame, 
# Returns Result: pandas.DataFrame as a result of overlapping synset counts
################################################################################
def ac_overlapping_terms_w_outer_matrix(df_doc_term_matrix, df_outer_matrix, idntfr):
    import pandas as pd
    import numpy as np

    t = df_doc_term_matrix.shape
    row_lgth = t[0]
    t = df_outer_matrix.shape
    row_lgth_o = t[0]
    outer_matrix_clm_count = []
    outer_matrix_clm_terms = []
    doc_term_matrix_index = df_doc_term_matrix.index
    outer_matrix_index = df_outer_matrix.index
    doc_term_matrix_clms = df_doc_term_matrix.columns

    for x in outer_matrix_index:
        # modified by Makoto.Sano@Mack-the-Psych.com 09/21/2020
        # s = 'Count_s_' + x
        s = 'Count_' + idntfr + '_' + x
        outer_matrix_clm_count.append(s)  

    for x in outer_matrix_index:
        # modified by Makoto.Sano@Mack-the-Psych.com 09/21/2020
        # s = 'Terms_s_' + x 
        s = 'Terms_' + idntfr + '_' + x
        outer_matrix_clm_terms.append(s)  
    
#    df_overlapping_matrix = pd.DataFrame(np.empty((row_lgth, row_lgth_o * 2),
#                    dtype=object), doc_term_matrix_index,
#                    outer_matrix_clm_count + outer_matrix_clm_terms)

    df_overlapping_count_matrix = pd.DataFrame(np.empty((row_lgth, row_lgth_o),
                    dtype=np.int64), doc_term_matrix_index,
                    outer_matrix_clm_count)

    df_overlapping_term_matrix = pd.DataFrame(np.empty((row_lgth, row_lgth_o),
                    dtype=object), doc_term_matrix_index,
                    outer_matrix_clm_terms)

    # modified by Makoto.Sano@Mack-the-Psych.com 09/20/2020
    '''
    df_overlapping_matrix = pd.concat([df_overlapping_count_matrix, df_overlapping_term_matrix], axis=1)

    for k, z in enumerate(doc_term_matrix_index):
        for i, x in enumerate(outer_matrix_clm_count):
            if k == i:
                #df_overlapping_matrix.iloc[k, i] = ''
                df_overlapping_matrix.iloc[k, i] = np.nan
            else:
                df_overlapping_matrix.iloc[k, i] = 0
                df_overlapping_matrix.iloc[k, i + len(outer_matrix_clm_count)] = ''
                for j, y in enumerate(df_outer_matrix.iloc[i, :]):
                    if y > 0:
                        if df_doc_term_matrix.iloc[k, j] > 0:
                            df_overlapping_matrix.iloc[k, i] += 1
                            s = df_overlapping_matrix.iloc[k, i + len(outer_matrix_clm_count)]
                            if s == '':
                                s = doc_term_matrix_clms[j]
                            else:
                                s = ';'.join([s, doc_term_matrix_clms[j]])
                            df_overlapping_matrix.iloc[k, i + len(outer_matrix_clm_count)] = s
    '''
    for k, z in enumerate(doc_term_matrix_index):
        for i, x in enumerate(outer_matrix_clm_count):
            if k == i:
                df_overlapping_count_matrix.iloc[k, i] = np.nan
            else:
                se_multiply = df_doc_term_matrix.iloc[k] * df_outer_matrix.iloc[i]
                se_match = se_multiply / se_multiply
                df_overlapping_count_matrix.iloc[k, i] = int(se_match.sum())

                se_match.index = df_doc_term_matrix.columns
                s = ';'.join(se_match[se_match > 0].index)
                df_overlapping_term_matrix.iloc[k, i] = s

    df_overlapping_matrix = pd.concat([df_overlapping_count_matrix, df_overlapping_term_matrix], axis=1)
    
    return df_overlapping_matrix
