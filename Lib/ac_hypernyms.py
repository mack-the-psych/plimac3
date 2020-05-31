################################################################################
# This module retrieves hypernyms from Wordnet as a part of NLTK module and its
# corpus. The module recognizes each input pandas.DataFrame record as a unit of 
# assessment content (i.e. a single passage section, an item stem, 
# or an item option) and applies a serial number of 'AC_Doc_ID' to the each
# output record for the following processing.
# Parameters df_ac: input pandas.DataFrame, it should have, at least, one 
#                   column of lemmatized text assessment content  
#            content_lemma_column: column name of lemmatized text assessment  
#                                  content (as an output text from the 
#                                  lemmatizer) to search Wordnet with the lemmas
# Returns Result: pandas.DataFrame including the original columns of the input 
#                 DataFrame plus result hypernyms
################################################################################
def ac_hypernyms(df_ac, content_lemma_column):
    import pandas as pd
    import numpy as np
    import nltk
    from nltk.corpus import wordnet as wn

    df_ac_buf = df_ac.copy()
    list_cntnt = list(df_ac_buf[content_lemma_column])
    list_cntnt_hypernyms = list_cntnt[:]
    list_doc_id = list_cntnt[:]    
    df_hypernyms_all = pd.DataFrame()

    for i, x in enumerate(list_cntnt):
        tokens = nltk.word_tokenize(x)
        hypernym_list = []
        for y in tokens:
            for synset in wn.synsets(y):
                #Updated 3/5/2017 mack.sano@gmail.com
                nltk_ver = list(map(int, nltk.__version__.split('.')))
                if (nltk_ver[0] > 2):
                    hypernyms = wn.synset(synset.name()).hypernyms()
                    for v in hypernyms:
                        hypernym_list = hypernym_list + v.lemma_names()
                else:
                    hypernyms = wn.synset(synset.name).hypernyms()
                    for v in hypernyms:
                        hypernym_list = hypernym_list + v.lemma_names
                    
        s = ' '.join(map(str,hypernym_list))
        list_cntnt_hypernyms[i] = s
        print(s)

        lower_hypernym_list = [w.lower() for w in hypernym_list]        
        df_hypernyms = pd.DataFrame({ 'Hypernyms' : lower_hypernym_list })
        df_doc = pd.DataFrame({ 'AC_Doc_ID' : np.array([i] * len(df_hypernyms)) })
        df_hypernyms['AC_Doc_ID'] = df_doc['AC_Doc_ID']
        df_hypernyms['Dummy'] = df_doc['AC_Doc_ID']
        df_hypernyms_all = df_hypernyms_all.append(df_hypernyms)
        list_doc_id[i] = i

    df_doc_id = pd.DataFrame({ 'AC_Doc_ID' : list_doc_id })
    df_ac_buf['AC_Doc_ID'] = df_doc_id['AC_Doc_ID']
    df_cntnt_hypernyms = pd.DataFrame({ 'Cntnt_Hypernyms' : list_cntnt_hypernyms })
    df_ac_buf['Cntnt_Hypernyms'] = df_cntnt_hypernyms['Cntnt_Hypernyms']

    #Updated 1/16/2017 mack.sano@gmail.com
    if df_hypernyms_all.shape[0] > 0:
        #Updated 3/5/2017 mack.sano@gmail.com
        pd_ver = list(map(int, pd.__version__.split('.')))
        if (pd_ver[0] > 0) or (pd_ver[1] > 13):
            df_crosstab = df_hypernyms_all.pivot_table(values='Dummy', 
                index='AC_Doc_ID', columns='Hypernyms', aggfunc = len)
        else:
            df_crosstab = df_hypernyms_all.pivot_table(values='Dummy',
                rows='AC_Doc_ID', cols='Hypernyms', aggfunc = len)

        df_crosstab['AC_Doc_ID'] = df_doc_id['AC_Doc_ID']
        df_res = pd.merge(df_ac_buf, df_crosstab, on='AC_Doc_ID', how='left')
    else:
        df_res = df_ac_buf

    return df_res.set_index('AC_Doc_ID')
