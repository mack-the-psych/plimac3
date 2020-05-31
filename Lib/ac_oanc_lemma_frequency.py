################################################################################
# This module calculates the mean/SD/min/max of the frequency of lemmas in 
# item stem and the options from the input lemma count columns in use of 
# the frequency information of OANC corpus. If the lemma count columns 
# of passage sections are also specified as the other input, the mean/SD/min/
# max of the frequency of lemmas in corresponded passage sections are also 
# calculated.
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
#            oanc_lemma: shelve of the frequency 
#                           information of OANC corpus, it should have 'Lemma'
#                           and the 'Count' (frequency) columns
#            stop_words = None: list of lemmas to specify stop words, they 
#                               should all include in the question and passage 
#                               DataFrames
#            unknown_word_len_min = 1: the minimum length of unknown lemma
#                                      which is recognized as UNKNOWN and 
#                                      asigned the lemma frequency as zero
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
#            decimal_places = None: specify the decimal places to round at
#            lang = 'En' : Language option ('En' or 'Jp')
# Returns Result: pandas.DataFrame reporting each 'AC_Doc_ID's lemma frequency 
#                 stats
################################################################################
def ac_oanc_lemma_frequency(df_ac_q, question_id_clm, stem_option_name_clm, 
                         lemma_start_q, oanc_lemma, stop_words = None,
                         unknown_word_len_min = 1, passage_name_clm_q = None, 
                         passage_sec_clm_q = None, df_ac_p = None, 
                         passage_name_clm_p = None, passage_sec_clm_p = None, 
                         lemma_start_p = None, decimal_places = None, lang = 'En'):
    import pandas as pd
    import numpy as np

    oanc_dic = oanc_lemma

    df_ac_buf = df_ac_q.copy()
    df_ac_id_buf = df_ac_buf[question_id_clm]
    df_ac_id = df_ac_id_buf.drop_duplicates()

    ac_buf_index_name = df_ac_buf.index.name
    ac_buf_index = df_ac_buf.index

    df_ac_buf = df_ac_buf.set_index([question_id_clm, stem_option_name_clm])
    df_ac_buf_lemma = df_ac_buf.iloc[:, (lemma_start_q - 2):]

    if stop_words != None:
        df_ac_buf_lemma = df_ac_buf_lemma.drop(stop_words, axis=1)

    if df_ac_p is not None:
        df_ac_buf_p = df_ac_p.copy()
        df_ac_buf_p = df_ac_buf_p.set_index([passage_name_clm_p, passage_sec_clm_p])

    df_res = pd.DataFrame()

    for x in df_ac_id:
        print('Question:' + str(x))
        ac_lemma_frq_passage = []

        if df_ac_p is not None:
            df_q_x = df_ac_buf.xs(x)
            # Modified by Sano.Makoto@otsuka.jp as a work around 4/20/2019            
            #passage_name = df_q_x.at[df_q_x.index[0], passage_name_clm_q]
            passage_name = df_q_x[passage_name_clm_q][0]
            #passage_sections = (df_q_x.at[df_q_x.index[0], passage_sec_clm_q]).split(';')
            passage_sections = (df_q_x[passage_sec_clm_q][0]).split(';')
            print('Passage:' + passage_name)
            df_p_x = df_ac_buf_p.xs(passage_name)
            df_p_x = df_p_x.loc[passage_sections]
            df_ac_buf_p_lemma_x = df_p_x.iloc[:, (lemma_start_p -2):]
            if stop_words != None:
                df_ac_buf_p_lemma_x = df_ac_buf_p_lemma_x.drop(stop_words, axis=1)
            df_ac_buf_p_lemma_x_sum = pd.DataFrame({ 'Passage' : df_ac_buf_p_lemma_x.sum() })
            # Modified by Sano.Makoto@otsuka.jp as a work around 4/20/2019
            #df_ac_buf_lemma_x = (df_ac_buf_lemma.xs(x)).append(df_ac_buf_p_lemma_x_sum.transpose())
            df_ac_buf_lemma_x = (df_ac_buf_p_lemma_x_sum.transpose()).append(df_ac_buf_lemma.xs(x))
            df_ac_buf_lemma_x.index.name = stem_option_name_clm
            df_ac_lemma_frq_doc = ac_oanc_lemma_frequency_dtm(df_ac_buf_lemma_x, oanc_dic,
                                                              unknown_word_len_min,
                                                              decimal_places, lang)

            ac_lemma_frq_passage = list(df_ac_lemma_frq_doc.loc['Passage', :])
            df_ac_lemma_frq_doc = df_ac_lemma_frq_doc.drop('Passage', axis=0)
        else:
            df_ac_lemma_frq_doc = ac_oanc_lemma_frequency_dtm(df_ac_buf_lemma.xs(x), 
                                                              oanc_dic,unknown_word_len_min,
                                                              decimal_places, lang)
        
        frq_clm_names = list(df_ac_lemma_frq_doc.columns)
        df_ac_lemma_frq_doc = df_ac_lemma_frq_doc.reset_index()
        df_doc = pd.DataFrame({ question_id_clm : np.array([x] *
                len(df_ac_lemma_frq_doc)) })
        df_ac_lemma_frq_doc[question_id_clm] = df_doc[question_id_clm]
        
        if df_ac_p is not None:
            for j, y in enumerate(frq_clm_names):
                passage_clm_name = 'Passage_' + str(y)
                df_frq_passage = pd.DataFrame({ passage_clm_name : np.array(
                                              [ac_lemma_frq_passage[j]] *
                                              len(df_ac_lemma_frq_doc)) })
                df_ac_lemma_frq_doc[passage_clm_name] = df_frq_passage[passage_clm_name]
        
        df_res = df_res.append(df_ac_lemma_frq_doc, ignore_index=True)

    df_doc_id = pd.DataFrame({ ac_buf_index_name : ac_buf_index })
    df_res[ac_buf_index_name] = df_doc_id[ac_buf_index_name]
    df_res = df_res.set_index(ac_buf_index_name)
    
    return df_res

################################################################################
# This module calculates the mean/SD/min/max of the frequency of lemmas from 
# the input lemma count columns in use of the frequency information of another
# input dictionary. 
# Parameters df_doc_term_matrix: input pandas.DataFrame of lemma count columns 
#                     with the index of the DataFrame
#            oanc_dic: a shelve which has lemmas as keys and the frequencies
#                      as values
#            unknown_word_len_min = 1: the length of unknown lemmas,
#                                      if the length of a lemma which does not 
#                                      include in the dictionary is equal to or 
#                                      greter than unknown_word_len_min,
#                                      the lemma is recognized as UNKNOWN and 
#                                      the term frequency will be zero, 
#                                      otherwise no frequency information will 
#                                      be provided as a part of the output.
#            decimal_places = None: specify the decimal places to round at
#            lang = 'En' : Language option ('En' or 'Jp')
# Returns Result: pandas.DataFrame reporting each record's lemma frequency stats
################################################################################
def ac_oanc_lemma_frequency_dtm(df_doc_term_matrix, oanc_dic, 
                                unknown_word_len_min = 1, 
                                decimal_places = None, lang = 'En'):
    import pandas as pd
    import numpy as np
    import shelve

    t = df_doc_term_matrix.shape
    row_lgth = t[0]
    col_lgth = t[1]
    doc_term_matrix_index = df_doc_term_matrix.index
    doc_term_matrix_clms = df_doc_term_matrix.columns

    df_lemma_frequency = pd.DataFrame(np.empty((row_lgth, 4),
                    dtype=np.float64), doc_term_matrix_index,
                    ['Lemma_Frq_Mean', 'Lemma_Frq_SD', 'Lemma_Frq_Max', 
                    'Lemma_Frq_Min'])

    for j, y in enumerate(doc_term_matrix_index):
        terms_frq = []
        for i, x in enumerate(list(doc_term_matrix_clms)):
            '''
            if lang == 'Jp':
                x = x.encode('utf-8')
            else:
                #Updated 4/9/2017 mack.sano@gmail.com
                x = x.encode()
            '''
            weight = df_doc_term_matrix.iloc[j, i]
            if str(weight) != 'nan':
                if  x in oanc_dic:
                    if str(oanc_dic[x]) != 'nan':
                        print('KNOWN: ' + x)
                        terms_frq = terms_frq + ([float(oanc_dic[x])] * int(weight))
                else:
                    '''
                    if lang == 'Jp':
                        length = len(x.decode('utf-8'))
                    else:
                        length = len(x)
                    '''
                    length = len(x)                   
                    if length >= unknown_word_len_min:
                        print('UNKNOWN: ' + x)
                        terms_frq = terms_frq + ([float(0.0)] * int(weight))
        
        term_count = len(terms_frq)
        print('TERM COUNT: ' + str(term_count))
        
        if term_count != 0:
            arr_term_frq = np.array(terms_frq)
            if decimal_places != None:
                df_lemma_frequency.iloc[j, 0] = round(np.average(arr_term_frq), decimal_places)
                df_lemma_frequency.iloc[j, 1] = round(np.std(arr_term_frq), decimal_places)
                df_lemma_frequency.iloc[j, 2] = round(np.max(arr_term_frq), decimal_places)
                df_lemma_frequency.iloc[j, 3] = round(np.min(arr_term_frq), decimal_places)
            else:
                df_lemma_frequency.iloc[j, 0] = np.average(arr_term_frq)
                df_lemma_frequency.iloc[j, 1] = np.std(arr_term_frq)
                df_lemma_frequency.iloc[j, 2] = np.max(arr_term_frq)
                df_lemma_frequency.iloc[j, 3] = np.min(arr_term_frq)
        else:
            df_lemma_frequency.iloc[j, 0] = 'nan'
            df_lemma_frequency.iloc[j, 1] = 'nan'
            df_lemma_frequency.iloc[j, 2] = 'nan'
            df_lemma_frequency.iloc[j, 3] = 'nan'

    return df_lemma_frequency

################################################################################
# This module loads the frequency information of OANC corpus  from CSV file
# into a shelve.
# Parameters file_name_r: CSV formated frequency information of OANC corpus, 
#                         it should have 'Lemma' and the 'Count' (frequency) 
#                         columns
#            file_name_w: output shelve file
#            lang = 'En' : Language option ('En' or 'Jp')
# Returns Result: None
################################################################################
def ac_load_oanc_shelve(file_name_r, file_name_w, lang = 'En'):
    import pandas as pd
    import shelve

    try:
        if lang == 'Jp':
            df_oanc_lemma = pd.read_csv(file_name_r, encoding='utf-8')
        else:
            df_oanc_lemma = pd.read_csv(file_name_r, encoding='latin-1')
        w = shelve.open(file_name_w, writeback=True)
    except Exception as e:
        print(e, 'error occurred')
    else:
        oanc_lemmas = list(df_oanc_lemma['Lemma'])

        print('Start writing OANC shelve')
        for i, x in enumerate(oanc_lemmas):
            '''
            if lang == 'Jp':
                x = x.encode('utf-8')
            else:
                x = str(x)
            '''
            x = str(x)
            #if w.has_key(x) == True:
            if x in w:
                w[x] = w[x] + df_oanc_lemma.at[df_oanc_lemma.index[i], 'Count']
            else:
                w[x] = df_oanc_lemma.at[df_oanc_lemma.index[i], 'Count']
        print('End writing OANC shelve')

    finally:
        w.close()

    return
