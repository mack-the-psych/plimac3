################################################################################
# This module retrieves synonyms from Wordnet as a part of NLTK module and its
# corpus. The module recognizes each input pandas.DataFrame record as a unit of 
# assessment content (i.e. a single passage section, an item stem, 
# or an item option) and applies a serial number of 'AC_Doc_ID' to the each
# output record for the following processing.
# Parameters df_ac: input pandas.DataFrame, it should have, at least, one 
#                   column of lemmatized text assessment content  
#            content_lemma_column: column name of lemmatized text assessment  
#                                  content (as an output text from the 
#                                  lemmatizer) to search Wordnet with the lemmas
#            lang = 'En' : Language option ('En' or 'Jp')
#            wnjpn_dic = None: dictionary of Japanese WordNet ('Jp' only)
# Returns Result: pandas.DataFrame including the original columns of the input 
#                 DataFrame plus result synsets, the result synsets include
#                 the original input lemmas as well
################################################################################
def ac_synset(df_ac, content_lemma_column, lang = 'En', wnjpn_dic = None):
    import pandas as pd
    import numpy as np

    if lang != 'Jp' or wnjpn_dic == None:
        import nltk
        from nltk.corpus import wordnet as wn

    df_ac_buf = df_ac.copy()
    list_cntnt = list(df_ac_buf[content_lemma_column])
    list_cntnt_synset = list_cntnt[:]
    list_doc_id = list_cntnt[:]    
    df_synset_all = pd.DataFrame()

    for i, x in enumerate(list_cntnt):
        if lang == 'Jp':
            tokens = x.split(' ')
            synset_list = tokens
            for y in tokens:
                if y in wnjpn_dic:
                    synset_list = synset_list + wnjpn_dic[y]

            #s = ' '.join(synset_list)
            s = ' '.join(map(str, synset_list))
            list_cntnt_synset[i] = s
            print(s)
            df_synset = pd.DataFrame({ 'Synset' : synset_list })
        else:
            tokens = nltk.word_tokenize(x)
            synset_list = tokens
            for y in tokens:
                for synset in wn.synsets(y):
                    synset_list = synset_list + synset.lemma_names()
            s = ' '.join(map(str, synset_list))
            list_cntnt_synset[i] = s
            print(s)
            lower_synset_list = [w.lower() for w in synset_list]
            df_synset = pd.DataFrame({ 'Synset' : lower_synset_list })

        df_doc = pd.DataFrame({ 'AC_Doc_ID' : np.array([i] * len(df_synset)) })
        df_synset['AC_Doc_ID'] = df_doc['AC_Doc_ID']
        df_synset['Dummy'] = df_doc['AC_Doc_ID']
        df_synset_all = df_synset_all.append(df_synset)
        list_doc_id[i] = i

    df_doc_id = pd.DataFrame({ 'AC_Doc_ID' : list_doc_id })
    df_ac_buf['AC_Doc_ID'] = df_doc_id['AC_Doc_ID']
    df_cntnt_synset = pd.DataFrame({ 'Cntnt_Synset' : list_cntnt_synset })
    df_ac_buf['Cntnt_Synset'] = df_cntnt_synset['Cntnt_Synset']

    #Updated 1/16/2017 mack.sano@gmail.com
    if df_synset_all.shape[0] > 0:
        #Updated 3/4/2017 mack.sano@gmail.com
        pd_ver = list(map(int, pd.__version__.split('.')))
        if (pd_ver[0] > 0) or (pd_ver[1] > 13):
            df_crosstab = df_synset_all.pivot_table(values='Dummy', 
                index='AC_Doc_ID', columns='Synset', aggfunc = len)
        else:
            df_crosstab = df_synset_all.pivot_table(values='Dummy', 
                rows='AC_Doc_ID', cols='Synset', aggfunc = len)
        df_crosstab['AC_Doc_ID'] = df_doc_id['AC_Doc_ID']
        df_res = pd.merge(df_ac_buf, df_crosstab, on='AC_Doc_ID')
    else:
        df_res = df_ac_buf

    return df_res.set_index('AC_Doc_ID')
