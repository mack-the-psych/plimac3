################################################################################
# This module aggregates the all psycho-linguistic measures into one matrix by
# each 'AC_Doc_ID (item stem or option). 
# Parameters df_ac_pos: input pandas.DataFrame, it should have, at least, POS 
#                       count columns with the 'AC_Doc_ID's as the index of
#                       the DataFrame
#            pos_start_q: integer column number (starting from zero) 
#                         specifying the starting point of POS count 
#                         columns in the question DataFrame, from the point 
#                         to the end, all the columns should be the POS count 
#                         columns
#            df_ac_loc_overlapping_lemma: pandas.DataFrame of the overlapping 
#                                         lemma location information, even no 
#                                             location information, still 
#                                             df_ac_overlapping_lemma is
#                                             acceptable
#            df_ac_loc_overlapping_syn_lemma: pandas.DataFrame of 
#                                             the overlapping lemma with synonym
#                                             location information, even no 
#                                             location information, still 
#                                             df_ac_overlapping_syn_lemma is
#                                             acceptable
#            df_ac_overlapping_nchunk: pandas.DataFrame as a result of 
#                                      overlapping NChunk counts
#            df_ac_oanc_lemma_freq_q: pandas.DataFrame reporting each 
#                                     'AC_Doc_ID's lemma frequency stats
#            stem_option_name_clm: column name of stem/option identifier 
#                                       in the aggregated DataFrame
#            stem_identifier: name of the stem identifier in the aggregated 
#                             DataFrame
#            keep_specific_columns_POS = None: a list of column names to be 
#                                              included into the aggrageted
#                                              matrix as a part of the original
#                                              columns of the df_ac_pos input
#                                              DataFrame
#            stop_words_POS = None: list of POS to specify stop words, they 
#                                   should all include in the POS question 
#                                   and passage DataFrames
#            df_ac_lemma_q = None: pandas.DataFrame of questions, it should 
#                     have, at least, lemma count columns with the 'AC_Doc_ID's   
#                     as the index of the DataFrame
#            include_specific_lemma_count = None: a list of lemmas to be 
#                                                 included into the aggrageted
#                                                 matrix as the lemma counts
#            df_ac_pos_p = None: pandas.DataFrame of passages, it should have,
#                     at least, POS count columns, passage name and the section
#                     columns
#            passage_name_clm_q = None: column name of the passage names 
#                                       in the lemma question DataFrame
#            passage_sec_clm_q = None: column name of the passage sections 
#                                       in the lemma question DataFrame
#            passage_name_clm_p = None: column name of the passage names 
#                                       in the passage DataFrame
#            passage_sec_clm_p = None: column name of the passage sections 
#                                       in the passage DataFrame
#            pos_start_p: integer column number (starting from zero) 
#                         specifying the starting point of POS count 
#                         columns in the passage DataFrame, from the point 
#                         to the end, all the columns should be the POS 
#                         count columns
#            decimal_places = None: specify the decimal places to round at
#            df_ac_overlapping_hypernyms = None: pandas.DataFrame as a result 
#                                         of overlapping hypernym counts
#            df_ac_overlapping_hyponyms = None: pandas.DataFrame as a result 
#                                         of overlapping hyponym counts
#            nchunk_suffix = '_nc': specify the suffix of NChunk variables
#                                   which was used for the column names of 
#                                   the overlapping NChunk
#            hypernym_suffix = '_hype': specify the suffix of hypernym variables
#                                   which was used for the column names of 
#                                   the overlapping hypernyms
#            hyponym_suffix = '_hypo': specify the suffix of hyponym variables
#                                   which was used for the column names of 
#                                   the overlapping hyponyms
#            df_ac_bigram_pmi_distribution = None: pandas.DataFrame as bigram
#                                                  PMI stats
#            df_ac_trigram_pmi_distribution = None: pandas.DataFrame as trigram
#                                                   PMI stats
# Returns Result: pandas.DataFrame including the original columns of 
#                 the df_ac_pos DataFrame plus aggregated result columns
################################################################################
def ac_aggregate_plim(df_ac_pos, pos_start_q, df_ac_loc_overlapping_lemma,
                      df_ac_loc_overlapping_syn_lemma, df_ac_overlapping_nchunk, 
                      df_ac_oanc_lemma_freq_q, stem_option_name_clm, stem_identifier, 
                      keep_specific_columns_POS = None, stop_words_POS = None,
                      df_ac_lemma_q = None, include_specific_lemma_count = None,
                      df_ac_pos_p = None, passage_name_clm_q = None, passage_sec_clm_q =None,
                      passage_name_clm_p = None, passage_sec_clm_p = None, 
                      pos_start_p = None, decimal_places = None,
                      df_ac_overlapping_hypernyms = None, df_ac_overlapping_hyponyms = None,
                      nchunk_suffix = '_nc', hypernym_suffix = '_hype', 
                      hyponym_suffix = '_hypo', df_ac_bigram_pmi_distribution = None,
                      df_ac_trigram_pmi_distribution = None):
    import pandas as pd

    df_ac_buf_POS = df_ac_pos.iloc[:, pos_start_q:]

    all_option_count_name_clms = []
    df_ac_options = df_ac_pos.drop_duplicates([stem_option_name_clm])

    for i, x in enumerate(df_ac_options[stem_option_name_clm]):
        if x != stem_identifier:
            s = 'Count_' + x
            all_option_count_name_clms.append(s)
    for i, x in enumerate(df_ac_options[stem_option_name_clm]):
        if x != stem_identifier:
            s = 'Count_s_' + x
            all_option_count_name_clms.append(s)
    for i, x in enumerate(df_ac_options[stem_option_name_clm]):
        if x != stem_identifier:
            s = 'Count' + nchunk_suffix + '_' + x
            all_option_count_name_clms.append(s)
    for i, x in enumerate(df_ac_options[stem_option_name_clm]):
        if x != stem_identifier:
            s = 'Count' + hypernym_suffix + '_' + x
            all_option_count_name_clms.append(s)
    for i, x in enumerate(df_ac_options[stem_option_name_clm]):
        if x != stem_identifier:
            s = 'Count' + hyponym_suffix + '_' + x
            all_option_count_name_clms.append(s)

    option_len = len(all_option_count_name_clms) // 5

    if stop_words_POS != None:
        df_ac_buf_POS = df_ac_buf_POS.drop(stop_words_POS, axis=1)
    
    df_ac_buf_sum = pd.DataFrame({ 'POS_sum' : df_ac_buf_POS.sum(axis=1) })
   
    if keep_specific_columns_POS != None:
        df_ac_buf_POS_head = df_ac_pos.loc[:, keep_specific_columns_POS]
    else:
        df_ac_buf_POS_head = df_ac_pos.copy()

    df_ac_buf_POS_head['POS_sum'] = df_ac_buf_sum['POS_sum']

    if df_ac_loc_overlapping_lemma is not None:
        df_concat = pd.concat([df_ac_buf_POS_head, df_ac_loc_overlapping_lemma], axis=1)
    else:
        df_concat = df_ac_buf_POS_head.copy()
    df_concat_tmp = df_concat.copy()

    if df_ac_loc_overlapping_syn_lemma is not None:
        df_concat = pd.concat([df_concat_tmp, df_ac_loc_overlapping_syn_lemma], axis=1)
        df_concat_tmp = df_concat.copy()

    if df_ac_overlapping_nchunk is not None:
        df_concat = pd.concat([df_concat_tmp, df_ac_overlapping_nchunk, df_ac_oanc_lemma_freq_q], axis=1)
    else:
        df_concat = pd.concat([df_concat_tmp, df_ac_oanc_lemma_freq_q], axis=1)
    df_concat_tmp = df_concat.copy()

    if df_ac_overlapping_hypernyms is not None:
        df_concat = pd.concat([df_concat_tmp, df_ac_overlapping_hypernyms], axis=1)
        df_concat_tmp = df_concat.copy()

    if df_ac_overlapping_hyponyms is not None:
        df_concat = pd.concat([df_concat_tmp, df_ac_overlapping_hyponyms], axis=1)
        df_concat_tmp = df_concat.copy()

    if df_ac_bigram_pmi_distribution is not None:
        df_concat = pd.concat([df_concat_tmp, df_ac_bigram_pmi_distribution], axis=1)
        df_concat_tmp = df_concat.copy()

    if df_ac_trigram_pmi_distribution is not None:
        df_concat = pd.concat([df_concat_tmp, df_ac_trigram_pmi_distribution], axis=1)
        df_concat_tmp = df_concat.copy()

    if df_ac_loc_overlapping_lemma is not None:
        df_ac_buf_sum = df_concat.loc[:, all_option_count_name_clms[0: option_len]]
        df_ac_buf_sum = pd.DataFrame({ 'Sum_Count_Options' : df_ac_buf_sum.sum(axis=1) })
        df_concat['Sum_Count_Options'] = df_ac_buf_sum['Sum_Count_Options']
    if df_ac_loc_overlapping_syn_lemma is not None:
        df_ac_buf_sum = df_concat.loc[:, all_option_count_name_clms[option_len: (option_len * 2)]]
        df_ac_buf_sum = pd.DataFrame({ 'Sum_Count_s_Options' : df_ac_buf_sum.sum(axis=1) })
        df_concat['Sum_Count_s_Options'] = df_ac_buf_sum['Sum_Count_s_Options']

    if df_ac_overlapping_nchunk is not None:
        df_ac_buf_sum = df_concat.loc[:, all_option_count_name_clms[(option_len * 2): (option_len * 3)]]
        clm_name = 'Sum_Count' + nchunk_suffix + '_Options'
        df_ac_buf_sum = pd.DataFrame({ clm_name : df_ac_buf_sum.sum(axis=1) })
        df_concat[clm_name] = df_ac_buf_sum[clm_name]
        
    if df_ac_overlapping_hypernyms is not None:
        df_ac_buf_sum = df_concat.loc[:, all_option_count_name_clms[(option_len * 3): (option_len * 4)]]
        clm_name = 'Sum_Count' + hypernym_suffix + '_Options'
        df_ac_buf_sum = pd.DataFrame({ clm_name : df_ac_buf_sum.sum(axis=1) })
        df_concat[clm_name] = df_ac_buf_sum[clm_name]

    if df_ac_overlapping_hyponyms is not None:
        df_ac_buf_sum = df_concat.loc[:, all_option_count_name_clms[(option_len * 4): (option_len * 5)]]
        clm_name = 'Sum_Count' + hyponym_suffix + '_Options'
        df_ac_buf_sum = pd.DataFrame({ clm_name : df_ac_buf_sum.sum(axis=1) })
        df_concat[clm_name] = df_ac_buf_sum[clm_name]
    
    if df_ac_lemma_q is not None:
        df_ac_buf_lemma_q = df_ac_lemma_q.loc[:, include_specific_lemma_count]
        df_ac_buf_lemma_q = df_ac_buf_lemma_q.fillna(0)
        for x in df_ac_buf_lemma_q.columns:
            df_concat['Lemma_Count_'+x] = df_ac_buf_lemma_q[x]

    if df_ac_pos_p is not None:
        df_res = ac_count_passage_pos_per_question(df_concat, passage_name_clm_q, passage_sec_clm_q, df_ac_pos_p,
                         passage_name_clm_p, passage_sec_clm_p, pos_start_p, stop_words_POS,)
    else:
        df_res = df_concat.copy()

    if 'Loc_Lemma_Mean' in df_res.columns:
        df_res['Std_Loc_Lemma_Mean'] = df_res['Loc_Lemma_Mean'] / df_res['Passage_POS_sum']
    if 'Loc_Synset_Mean' in df_res.columns:
        df_res['Std_Loc_Synset_Mean'] = df_res['Loc_Synset_Mean'] / df_res['Passage_POS_sum']
    
    if df_ac_pos_p is not None:
        df_res['Std_Count_Passage'] = df_res['Count_Passage'] / df_res['Passage_POS_sum']
        df_res['Std_Count_s_Passage'] = df_res['Count_s_Passage'] / df_res['Passage_POS_sum']

        clm_name = 'Count' + nchunk_suffix + '_Passage'
        if clm_name in df_res.columns:
            df_res['Std_' + clm_name] = df_res[clm_name] / df_res['Passage_POS_sum']

        clm_name = 'Count' + hypernym_suffix + '_Passage'
        if clm_name in df_res.columns:
            df_res['Std_' + clm_name] = df_res[clm_name] / df_res['Passage_POS_sum']

        clm_name = 'Count' + hyponym_suffix + '_Passage'
        if clm_name in df_res.columns:
            df_res['Std_' + clm_name] = df_res[clm_name] / df_res['Passage_POS_sum']

        df_res['Std_POS_sum'] = df_res['POS_sum'] / df_res['Passage_POS_sum']

    if decimal_places != None:
        for x in df_res.index:
            if 'Loc_Lemma_Mean' in df_res.columns:
                df_res.loc[x, 'Std_Loc_Lemma_Mean'] = round(df_res.loc[x, 'Std_Loc_Lemma_Mean'], decimal_places)
            if 'Loc_Synset_Mean' in df_res.columns:
                df_res.loc[x, 'Std_Loc_Synset_Mean'] = round(df_res.loc[x, 'Std_Loc_Synset_Mean'], decimal_places)
            if df_ac_pos_p is not None:
                df_res.loc[x, 'Std_Count_Passage'] = round(df_res.loc[x, 'Std_Count_Passage'], decimal_places)
                df_res.loc[x, 'Std_Count_s_Passage'] = round(df_res.loc[x, 'Std_Count_s_Passage'], decimal_places)

                clm_name = 'Std_Count' + nchunk_suffix + '_Passage'
                if clm_name in df_res.columns:
                    df_res.loc[x, clm_name] = round(df_res.loc[x, clm_name], decimal_places)

                clm_name = 'Std_Count' + hypernym_suffix + '_Passage'
                if clm_name in df_res.columns:
                    df_res.loc[x, clm_name] = round(df_res.loc[x, clm_name], decimal_places)

                clm_name = 'Std_Count' + hyponym_suffix + '_Passage'
                if clm_name in df_res.columns:
                    df_res.loc[x, clm_name] = round(df_res.loc[x, clm_name], decimal_places)

                df_res.loc[x, 'Std_POS_sum'] = round(df_res.loc[x, 'Std_POS_sum'], decimal_places)
    else:
        for x in df_res.index:
            if 'Loc_Lemma_Mean' in df_res.columns:
                df_res.loc[x, 'Std_Loc_Lemma_Mean'] = df_res.loc[x, 'Std_Loc_Lemma_Mean']
            if 'Loc_Synset_Mean' in df_res.columns:
                df_res.loc[x, 'Std_Loc_Synset_Mean'] = df_res.loc[x, 'Std_Loc_Synset_Mean']
            if df_ac_pos_p is not None:
                df_res.loc[x, 'Std_Count_Passage'] = df_res.loc[x, 'Std_Count_Passage']
                df_res.loc[x, 'Std_Count_s_Passage'] = df_res.loc[x, 'Std_Count_s_Passage']

                clm_name = 'Std_Count' + nchunk_suffix + '_Passage'
                if clm_name in df_res.columns:
                    df_res.loc[x, clm_name] = df_res.loc[x, clm_name]

                clm_name = 'Std_Count' + hypernym_suffix + '_Passage'
                if clm_name in df_res.columns:
                    df_res.loc[x, clm_name] = df_res.loc[x, clm_name]

                clm_name = 'Std_Count' + hyponym_suffix + '_Passage'
                if clm_name in df_res.columns:
                    df_res.loc[x, clm_name] = df_res.loc[x, clm_name]

                df_res.loc[x, 'Std_POS_sum'] = df_res.loc[x, 'Std_POS_sum']
    
    return df_res

################################################################################
# This module counts the total number of POS in the corresponsed passage(s) of 
# each question.
# Parameters df_ac_q: input pandas.DataFrame of questions, it should have,  
#                     at least the 'AC_Doc_ID's as the index of the DataFrame,
#                     the DataFrame of questions should also have corresponded
#                     passage name and the section columns
#            passage_name_clm_q: column name of the passage names 
#                                       in the question DataFrame
#            passage_sec_clm_q: column name of the passage sections 
#                                       in the question DataFrame
#            df_ac_p: input pandas.DataFrame of passages, it should have,
#                     at least, POS count columns, passage name and the section
#                     columns
#            passage_name_clm_p: column name of the passage names 
#                                in the passage DataFrame
#            passage_sec_clm_p: column name of the passage sections 
#                               in the passage DataFrame
#            pos_start_p: integer column number (starting from zero) 
#                         specifying the starting point of POS count 
#                         columns in the passage DataFrame, from the point 
#                         to the end, all the columns should be the POS 
#                         count columns
#            stop_words = None: list of lemmas to specify stop words, they 
#                               should all include in the question and passage 
#                               DataFrames
# Returns Result: pandas.DataFrame including the original columns of the input 
#                 DataFrame plus the result of the POS counts of 
#                 the corresponsed passage(s)
################################################################################
def ac_count_passage_pos_per_question(df_ac_q, passage_name_clm_q, 
                         passage_sec_clm_q, df_ac_p, passage_name_clm_p, 
                         passage_sec_clm_p,pos_start_p,
                         stop_words_pos = None):
    import pandas as pd
    import numpy as np

    df_ac_buf = df_ac_q.copy()
    ac_buf_index = df_ac_buf.index
    ac_buf_index_name = df_ac_buf.index.name

    df_ac_buf_p = df_ac_p.copy()
    df_ac_buf_p_POS = df_ac_buf_p.iloc[:, pos_start_p:]
    df_q_POS_all = pd.DataFrame()

    if stop_words_pos != None:
        df_ac_buf_p_POS = df_ac_buf_p_POS.drop(stop_words_pos, axis=1)

    df_ac_buf_p_POS_sum = pd.DataFrame({ 'POS_sum' : df_ac_buf_p_POS.sum(axis=1) })
    df_ac_buf_p['POS_sum'] = df_ac_buf_p_POS_sum['POS_sum']
    df_ac_buf_p = df_ac_buf_p.set_index([passage_name_clm_p, passage_sec_clm_p])

    for x in ac_buf_index:
        passage_name = df_ac_buf.loc[x, passage_name_clm_q]
        passage_sections = (df_ac_buf.loc[x, passage_sec_clm_q]).split(';')
        df_p_x = df_ac_buf_p.xs(passage_name)
        df_p_x = df_p_x.loc[passage_sections]
        df_ac_buf_p_POS_x = df_p_x.loc[:, ['POS_sum']]
        df_ac_buf_p_POS_x_sum = pd.DataFrame({ 'Passage_POS_sum' : 
                                             df_ac_buf_p_POS_x.sum()})
        df_q_POS_all = df_q_POS_all.append(df_ac_buf_p_POS_x_sum, ignore_index = True)

    df_ac_buf = df_ac_buf.reset_index()
    df_ac_buf['Passage_POS_sum'] = df_q_POS_all['Passage_POS_sum']
    df_ac_buf = df_ac_buf.set_index(ac_buf_index_name)

    return df_ac_buf
