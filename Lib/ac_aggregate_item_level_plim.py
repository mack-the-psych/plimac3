################################################################################
# This module restructures the item-level psycho-linguistic measures from
# the all psycho-linguistic measures into one matrix by each item.
# Parameters df_ac_aggregated: input pandas.DataFrame as a result of 
#                              the all aggregated psycho-linguistic measures.
#                              it should includes the item key information and 
#                              stem/option identifier columns
#            key_clm = None: column name of the item key information column
#                                       in the aggregated DataFrame
#            stem_option_name_clm: column name of stem/option identifier 
#                                       in the aggregated DataFrame
#            stem_identifier: name of the stem identifier in the aggregated 
#                             DataFrame
#            include_specific_stem_lemma_count = None: a list of lemmas to be 
#                                                 included into the aggrageted
#                                                 matrix as the stem lemma 
#                                                 counts
#            decimal_places = None: specify the decimal places to round at
#            content_column = None: column name of text assessment content 
#                                   if the content columns of stems need to be 
#                                   included
#            nchunk_suffix = '_nc': specify the suffix of NChunk variables
#                                   which was used for the columns name of 
#                                   the overlapping NChunk
#            hypernym_suffix = '_hype': specify the suffix of hypernym variables
#                                   which was used for the column names of 
#                                   the overlapping hypernyms
#            hyponym_suffix = '_hypo': specify the suffix of hyponym variables
#                                   which was used for the column names of 
#                                   the overlapping hyponyms
# Returns Result: pandas.DataFrame including the original columns of 
#                 the aggregated DataFrame plus restructured result columns
################################################################################
def ac_aggregate_item_level_plim(df_ac_aggregated, key_clm, stem_option_name_clm, 
                                 stem_identifier, 
                                 include_specific_stem_lemma_count = None, 
                                 decimal_places = None, content_column = None,
                                 nchunk_suffix = '_nc', hypernym_suffix = '_hype',
                                 hyponym_suffix = '_hypo'):
    import pandas as pd

    df_ac_buf = df_ac_aggregated.loc[:, [key_clm, stem_option_name_clm]]
    
    df_plim_key = pd.DataFrame()
    for i, x in enumerate(df_ac_buf[key_clm]):
        if x == df_ac_buf.iloc[i, 1]:
            df_ac_aggregated_buf = df_ac_aggregated[i: (i + 1)]
            df_plim_key = df_plim_key.append(df_ac_aggregated_buf)
    
    df_plim_key.index.name = 'AC_Doc_ID'
    
    df_plim_stem = pd.DataFrame()
    for i, x in enumerate(df_ac_buf[stem_option_name_clm]):
        if x == stem_identifier:
            df_ac_aggregated_buf = df_ac_aggregated[i: (i + 1)]
            df_plim_stem = df_plim_stem.append(df_ac_aggregated_buf)
    
    df_plim_stem.index.name = 'AC_Doc_ID'
    
    df_plim = df_plim_key.copy()
    df_plim = df_plim.reset_index()
    df_buf_plim_stem = df_plim_stem.reset_index()
    if content_column != None:
        df_plim['Stem_'+content_column] = df_buf_plim_stem[content_column]
    df_plim['Stem_POS_sum'] = df_buf_plim_stem['POS_sum']
    if 'Count_Passage' in df_buf_plim_stem.columns:
        df_plim['Stem_Count_Passage'] = df_buf_plim_stem['Count_Passage']
        df_plim['Stem_Count_s_Passage'] = df_buf_plim_stem['Count_s_Passage']

    if 'PMI_Bigram_Mean' in df_buf_plim_stem.columns:
        df_plim['Stem_PMI_Bigram_Mean'] = df_buf_plim_stem['PMI_Bigram_Mean']
        df_plim['Stem_PMI_Bigram_SD'] = df_buf_plim_stem['PMI_Bigram_SD']
        df_plim['Stem_PMI_Bigram_Max'] = df_buf_plim_stem['PMI_Bigram_Max']
        df_plim['Stem_PMI_Bigram_Min'] = df_buf_plim_stem['PMI_Bigram_Min']

    if 'PMI_Trigram_Mean' in df_buf_plim_stem.columns:
        df_plim['Stem_PMI_Trigram_Mean'] = df_buf_plim_stem['PMI_Trigram_Mean']
        df_plim['Stem_PMI_Trigram_SD'] = df_buf_plim_stem['PMI_Trigram_SD']
        df_plim['Stem_PMI_Trigram_Max'] = df_buf_plim_stem['PMI_Trigram_Max']
        df_plim['Stem_PMI_Trigram_Min'] = df_buf_plim_stem['PMI_Trigram_Min']

    clm_name = 'Count' + nchunk_suffix + '_Passage'
    if clm_name in df_buf_plim_stem.columns:
        df_plim['Stem_' + clm_name] = df_buf_plim_stem[clm_name]

    clm_name = 'Count' + hypernym_suffix + '_Passage'
    if clm_name in df_buf_plim_stem.columns:
        df_plim['Stem_' + clm_name] = df_buf_plim_stem[clm_name]

    clm_name = 'Count' + hyponym_suffix + '_Passage'
    if clm_name in df_buf_plim_stem.columns:
        df_plim['Stem_' + clm_name] = df_buf_plim_stem[clm_name]

    df_plim['Stem_Sum_Count_Options'] = df_buf_plim_stem['Sum_Count_Options']
    df_plim['Stem_Sum_Count_s_Options'] = df_buf_plim_stem['Sum_Count_s_Options']

    clm_name = 'Sum_Count' + nchunk_suffix + '_Options'
    if clm_name in df_buf_plim_stem.columns:
        df_plim['Stem_' + clm_name] = df_buf_plim_stem[clm_name]

    clm_name = 'Sum_Count' + hypernym_suffix + '_Options'
    if clm_name in df_buf_plim_stem.columns:
        df_plim['Stem_' + clm_name] = df_buf_plim_stem[clm_name]

    clm_name = 'Sum_Count' + hyponym_suffix + '_Options'
    if clm_name in df_buf_plim_stem.columns:
        df_plim['Stem_' + clm_name] = df_buf_plim_stem[clm_name]

    if 'Loc_Lemma_Mean' in df_buf_plim_stem.columns:
        df_plim['Stem_Loc_Lemma_Mean'] = df_buf_plim_stem['Loc_Lemma_Mean']
        df_plim['Stem_Loc_Lemma_SD'] = df_buf_plim_stem['Loc_Lemma_SD']
        df_plim['Stem_Loc_Synset_Mean'] = df_buf_plim_stem['Loc_Synset_Mean']
        df_plim['Stem_Loc_Synset_SD'] = df_buf_plim_stem['Loc_Synset_SD']

    if include_specific_stem_lemma_count is not None:
        for x in include_specific_stem_lemma_count:
            df_plim['Stem_Lemma_Count_'+x] = df_buf_plim_stem['Lemma_Count_'+x]

    df_plim['Stem_Lemma_Frq_Max'] = df_buf_plim_stem['Lemma_Frq_Max']
    df_plim['Stem_Lemma_Frq_Mean'] = df_buf_plim_stem['Lemma_Frq_Mean']
    df_plim['Stem_Lemma_Frq_Min'] = df_buf_plim_stem['Lemma_Frq_Min']
    df_plim['Stem_Lemma_Frq_SD'] = df_buf_plim_stem['Lemma_Frq_SD']
    if 'Count_Passage' in df_buf_plim_stem.columns:
        df_plim['Std_Stem_Count_Passage'] = df_buf_plim_stem['Std_Count_Passage']
        df_plim['Std_Stem_Count_s_Passage'] = df_buf_plim_stem['Std_Count_s_Passage']
        df_plim['Std_Stem_POS_sum'] = df_buf_plim_stem['Std_POS_sum']

    clm_name = 'Std_Count' + nchunk_suffix + '_Passage'
    if clm_name in df_buf_plim_stem.columns:
        df_plim['Std_Stem_Count' + nchunk_suffix + '_Passage'] = df_buf_plim_stem[clm_name]

    clm_name = 'Std_Count' + hypernym_suffix + '_Passage'
    if clm_name in df_buf_plim_stem.columns:
        df_plim['Std_Stem_Count' + hypernym_suffix + '_Passage'] = df_buf_plim_stem[clm_name]

    clm_name = 'Std_Count' + hyponym_suffix + '_Passage'
    if clm_name in df_buf_plim_stem.columns:
        df_plim['Std_Stem_Count' + hyponym_suffix + '_Passage'] = df_buf_plim_stem[clm_name]

    all_option_count_name_clms = []
    df_ac_options = df_ac_buf.drop_duplicates([stem_option_name_clm])

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
            if s in df_plim.columns:
                all_option_count_name_clms.append(s)
    for i, x in enumerate(df_ac_options[stem_option_name_clm]):
        if x != stem_identifier:
            s = 'Count' + hypernym_suffix + '_' + x
            if s in df_plim.columns:
                all_option_count_name_clms.append(s)
    for i, x in enumerate(df_ac_options[stem_option_name_clm]):
        if x != stem_identifier:
            s = 'Count' + hyponym_suffix + '_' + x
            if s in df_plim.columns:
                all_option_count_name_clms.append(s)

    df_plim = df_plim.drop(all_option_count_name_clms, axis=1)
    
    if 'Loc_Lemma_Mean' in df_buf_plim_stem.columns:
        df_plim['Dist_Lemma_Stem_Passage'] = (df_plim['Loc_Lemma_Mean'] 
                                             - df_buf_plim_stem['Loc_Lemma_Mean']).abs()
        df_plim['Dist_Synset_Stem_Passage'] = (df_plim['Loc_Synset_Mean'] 
                                             - df_buf_plim_stem['Loc_Synset_Mean']).abs()
    
    df_plim = df_plim.set_index('AC_Doc_ID')

    #Updated 5/7/2017 mack.sano@gmail.com
    #if 'Passage_POS_sum' in df_plim.columns:
    if 'Dist_Lemma_Stem_Passage' in df_plim.columns:        
        df_plim['Std_Dist_Lemma_Stem_Passage'] = df_plim['Dist_Lemma_Stem_Passage'] / df_plim['Passage_POS_sum']
        df_plim['Std_Dist_Synset_Stem_Passage'] = df_plim['Dist_Synset_Stem_Passage'] / df_plim['Passage_POS_sum']

    if decimal_places != None:
        for x in df_plim.index:
            #Updated 5/7/2017 mack.sano@gmail.com
            #if 'Passage_POS_sum' in df_plim.columns:
            if 'Dist_Lemma_Stem_Passage' in df_plim.columns:                
                df_plim.loc[x, 'Dist_Lemma_Stem_Passage'] = round(df_plim.loc[x, 'Dist_Lemma_Stem_Passage'], decimal_places)
                df_plim.loc[x, 'Dist_Synset_Stem_Passage'] = round(df_plim.loc[x, 'Dist_Synset_Stem_Passage'], decimal_places)
                df_plim.loc[x, 'Std_Dist_Lemma_Stem_Passage'] = round(df_plim.loc[x, 'Std_Dist_Lemma_Stem_Passage'], decimal_places)
                df_plim.loc[x, 'Std_Dist_Synset_Stem_Passage'] = round(df_plim.loc[x, 'Std_Dist_Synset_Stem_Passage'], decimal_places)
    else:
        for x in df_plim.index:
            #Updated 5/7/2017 mack.sano@gmail.com
            #if 'Passage_POS_sum' in df_plim.columns:
            if 'Dist_Lemma_Stem_Passage' in df_plim.columns:                
                df_plim.loc[x, 'Dist_Lemma_Stem_Passage'] = df_plim.loc[x, 'Dist_Lemma_Stem_Passage']
                df_plim.loc[x, 'Dist_Synset_Stem_Passage'] = df_plim.loc[x, 'Dist_Synset_Stem_Passage']
                df_plim.loc[x, 'Std_Dist_Lemma_Stem_Passage'] = df_plim.loc[x, 'Std_Dist_Lemma_Stem_Passage']
                df_plim.loc[x, 'Std_Dist_Synset_Stem_Passage'] = df_plim.loc[x, 'Std_Dist_Synset_Stem_Passage']

    return df_plim
