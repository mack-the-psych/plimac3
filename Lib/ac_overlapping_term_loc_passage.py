################################################################################
# This module locates the lemmas in the passage, overlapping with the lemmas/
# synonyms in the corresponded options or the item stem, and compute 
# the mean and SD of the location in the passage by each option or item stem.
# Parameters df_ac_q: input pandas.DataFrame of questions, it should have the 
#                     'AC_Doc_ID's as the index of the DataFrame, the question
#                     ID column, and stem/option identifier column, 
#                     the DataFrame of questions should also have corresponded 
#                     passage name and the section columns, the module assumes 
#                     that the stem and options which have the same question 
#                     ID share the same passage name and the section(s)
#            question_id_clm: column name of question IDs in the lemma question 
#                             DataFrame which are shared by the item stem and 
#                             the options of each question 
#            stem_option_name_clm: column name of stem/option identifier  
#                             in the lemma question DataFrame
#            passage_name_clm_q: column name of the passage names in the lemma
#                                question DataFrame
#            passage_sec_clm_q: column name of the passage sections 
#                               in the lemma question DataFrame
#            df_ac_p: input pandas.DataFrame of passages, it should have,
#                     at least, the lemmatized content column, passage name 
#                     and the section columns
#            passage_name_clm_p: column name of the passage names 
#                                       in the passage DataFrame
#            passage_sec_clm_p: column name of the passage sections 
#                                       in the passage DataFrame
#            cntnt_lemma_clm_p: column name of the lemmatized passage content
#                               as a part of the lemmatizer output
#            df_ac_q_ovlp_lemma: input pandas.DataFrame as a result of 
#                                overlapping lemma counts
#            ovlp_lemma_clm_q: column name of the list of overlapping lemmas
#            mean_clm_title: output column name of the mean of the location 
#                            in the passage
#            sd_clm_title: output column name of the SD of the location 
#                          in the passage
#            max_term_loc_sd = None: the upper limit of the SD of the individual 
#                                    lemma/synonym's location which will be 
#                                    included in the overall mean and SD 
#                                    calculations
#            decimal_places = None: specify the decimal places to round at
#            lang = 'En' : Language option ('En' or 'Jp')
# Returns Result: pandas.DataFrame of the overlapping lemma location information
################################################################################
def ac_overlapping_term_loc_passage(df_ac_q, question_id_clm, stem_option_name_clm, 
                         passage_name_clm_q, passage_sec_clm_q,
                         df_ac_p, passage_name_clm_p, passage_sec_clm_p,
                         cntnt_lemma_clm_p, df_ac_q_ovlp_lemma, ovlp_lemma_clm_q,
                         mean_clm_title, sd_clm_title, max_term_loc_sd = None, 
                                    decimal_places = None, lang = 'En'):
    import pandas as pd
    import numpy as np

    df_ac_buf_q_ovlp = df_ac_q_ovlp_lemma.copy()
    df_ac_id_buf = df_ac_buf_q_ovlp[question_id_clm]
    df_ac_id = df_ac_id_buf.drop_duplicates()

    ac_buf_index_name = df_ac_buf_q_ovlp.index.name
    ac_buf_index = df_ac_buf_q_ovlp.index
    df_ac_buf_q_ovlp = df_ac_buf_q_ovlp.reset_index()
    df_ac_buf_q_ovlp = df_ac_buf_q_ovlp.set_index([question_id_clm, stem_option_name_clm])

    df_ac_buf_q = df_ac_q.copy()
    df_ac_buf_q = df_ac_buf_q.set_index([question_id_clm, stem_option_name_clm])

    df_ac_buf_p = df_ac_p.copy()
    df_ac_buf_p = df_ac_buf_p.set_index([passage_name_clm_p, passage_sec_clm_p])

    df_res = pd.DataFrame()

    for x in df_ac_id:
        print('Question:' + str(x))

        df_q_x = df_ac_buf_q.xs(x)
        # Modified by Sano.Makoto@otsuka.jp as a work around 4/20/2019
        #passage_name = df_q_x.at[df_q_x.index[0], passage_name_clm_q]
        passage_name = df_q_x[passage_name_clm_q][0]
        #passage_sections = (df_q_x.at[df_q_x.index[0], passage_sec_clm_q]).split(';')
        passage_sections = (df_q_x[passage_sec_clm_q][0]).split(';')

        df_q_ovlp_x = df_ac_buf_q_ovlp.xs(x)

        print('Passage:' + passage_name)
        df_p_x = df_ac_buf_p.xs(passage_name)
        df_p_x = df_p_x.loc[passage_sections]
        
        df_ac_overlap_loc = ac_question_ovlp_term_loc_passage(df_p_x, 
                                cntnt_lemma_clm_p, df_q_ovlp_x, ovlp_lemma_clm_q,
                                mean_clm_title, sd_clm_title, max_term_loc_sd,
                                decimal_places, lang)
        df_ac_overlap_loc = df_ac_overlap_loc.reset_index()
        df_doc = pd.DataFrame({ question_id_clm : np.array([x] *
                len(df_ac_overlap_loc)) })
        df_ac_overlap_loc[question_id_clm] = df_doc[question_id_clm]
        df_res = df_res.append(df_ac_overlap_loc, ignore_index=True)

    df_doc_id = pd.DataFrame({ ac_buf_index_name : ac_buf_index })
    df_res[ac_buf_index_name] = df_doc_id[ac_buf_index_name]
    
    df_merge = pd.merge(df_ac_buf_q_ovlp, df_res, on=ac_buf_index_name)

    return df_merge.set_index(ac_buf_index_name)

################################################################################
# This module locates the lemmas in the input passage(s), matching with 
# the listed lemmas/synonyms by each option or item stem, and compute the mean 
# and SD of the location in the passage by each option or item stem.
# Parameters df_ac_p: input pandas.DataFrame of passages, it should have,
#                     at least, the lemmatized content column
#            cntnt_lemma_clm_p: column name of the lemmatized passage content
#                               as a part of the lemmatizer output
#            df_ac_q_ovlp_lemma: input pandas.DataFrame as a result of 
#                                overlapping lemma counts
#            ovlp_lemma_clm_q: column name of the list of overlapping lemmas
#            mean_clm_title: output column name of the mean of the location 
#                            in the passage
#            sd_clm_title: output column name of the SD of the location 
#                          in the passage
#            max_term_loc_sd = None: the upper limit of the SD of the individual 
#                                    lemma/synonym's location which will be 
#                                    included in the overall mean and SD 
#                                    calculations
#            decimal_places = None: specify the decimal places to round at
#            lang = 'En' : Language option ('En' or 'Jp')
# Returns Result: pandas.DataFrame of the overlapping lemma location information
################################################################################
def ac_question_ovlp_term_loc_passage(df_ac_p, cntnt_lemma_clm_p, 
                                    df_ac_q_ovlp_lemma, ovlp_lemma_clm_q,
                                    mean_clm_title, sd_clm_title, 
                                    max_term_loc_sd = None, 
                                    decimal_places = None, lang = 'En'):
    import pandas as pd
    import numpy as np

    t = df_ac_q_ovlp_lemma.shape
    row_lgth = t[0]
    ac_q_ovlp_lemm_index = df_ac_q_ovlp_lemma.index

    df_question_ovlp_tem_loc = pd.DataFrame(np.empty((row_lgth, 2),
                    dtype=np.float64), ac_q_ovlp_lemm_index,
                    [mean_clm_title, sd_clm_title])

    list_cntnt = list(df_ac_p[cntnt_lemma_clm_p])
    cntnt_all = ' '.join(list_cntnt)
    passage_terms = cntnt_all.split(' ')

    cntnt_dic = {}

    for i, x in enumerate(passage_terms):
        if x in cntnt_dic:
            cntnt_dic[x].append(i)
        else:
            cntnt_dic[x] = [i]

    list_ovlp_lemma = list(df_ac_q_ovlp_lemma[ovlp_lemma_clm_q])

    for i, x in enumerate(list_ovlp_lemma):
        flg_terms = False

        '''
        if lang == 'Jp':
            import types
            if type(x) != types.FloatType:
                print('OVERLAPPING TERMS:' + x.encode('utf-8'))
                stem_terms = x.split(';')
                flg_terms = True
        else:
            s = str(x)
            if s != 'nan' and s != '':
                print('OVERLAPPING TERMS:' + s)
                stem_terms = s.split(';')
                flg_terms = True
        '''

        s = str(x)
        if s != 'nan' and s != '':
            print('OVERLAPPING TERMS:' + s)
            stem_terms = s.split(';')
            flg_terms = True

        if flg_terms == True:
            stem_terms_loc = []
            for y in stem_terms:
                print(y)
                print(cntnt_dic[y])
                arr_term_loc = np.array(cntnt_dic[y])
                
                if max_term_loc_sd != None:
                    if np.std(arr_term_loc) <= max_term_loc_sd:
                        stem_terms_loc = stem_terms_loc + cntnt_dic[y]
                else:
                    stem_terms_loc = stem_terms_loc + cntnt_dic[y]

            print('ALL LOCATIONS:' + str(stem_terms_loc))

            arr_all_terms_loc = np.array(stem_terms_loc)
            if decimal_places != None:
                df_question_ovlp_tem_loc.iloc[i, 0] = round(np.average(arr_all_terms_loc), decimal_places)
                df_question_ovlp_tem_loc.iloc[i, 1] = round(np.std(arr_all_terms_loc), decimal_places)
            else:
                df_question_ovlp_tem_loc.iloc[i, 0] = np.average(arr_all_terms_loc)
                df_question_ovlp_tem_loc.iloc[i, 1] = np.std(arr_all_terms_loc)            
        else:
            df_question_ovlp_tem_loc.iloc[i, 0] = 'nan'
            df_question_ovlp_tem_loc.iloc[i, 1] = 'nan'

    return df_question_ovlp_tem_loc
