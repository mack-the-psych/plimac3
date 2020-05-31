################################################################################
# This module lemmatizes the text in the specified column of the input
# pandas.DataFrame. The module recognizes each input record as a unit of 
# assessment content (i.e. a single passage section, an item stem, 
# or an item option) and applies a serial number of 'AC_Doc_ID' to the each
# output record for the following processing.
# Parameters df_ac: input pandas.DataFrame, it should have, at least, one 
#                   column of text assessment content  
#            content_column: column name of text assessment content to be 
#                            lemmatized
#            lang = 'En' : Language option ('En' or 'Jp')
# Returns Result: pandas.DataFrame including the original columns of the input 
#                 DataFrame plus lemmatized result columns
################################################################################
def ac_lemmatizer(df_ac, content_column, lang = 'En'):
    import pandas as pd
    import numpy as np

    if lang == 'Jp':
        from janome.tokenizer import Tokenizer
        tagger = Tokenizer()
    else:
        import nltk
        wnl = nltk.WordNetLemmatizer()
        import nltk.data
        sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')

    df_ac_buf = df_ac.copy()
    list_cntnt = list(df_ac_buf[content_column])
    list_cntnt_lemma = list_cntnt[:]
    list_doc_id = list_cntnt[:]    
    df_lemma_all = pd.DataFrame()

    if lang == 'Jp':
        for i, x in enumerate(list_cntnt):
            lemmas = []
            sentences = x.splitlines()
            for y in sentences:
                for token in tagger.tokenize(y.strip()):
                    surface = token.surface
                    feature = token.part_of_speech
                    feature_list = feature.split(',')
                    if surface != u' ':
                        if token.base_form != u'*':
                            lemmas = lemmas + [token.base_form]
                        else:
                            lemmas = lemmas + [surface]
            
            s = ' '.join(lemmas)
            list_cntnt_lemma[i] = s
            print(s)
            df_lemma = pd.DataFrame({ 'Lemma' : lemmas })
            df_doc = pd.DataFrame({ 'AC_Doc_ID' : np.array([i] * len(df_lemma)) })
            df_lemma['AC_Doc_ID'] = df_doc['AC_Doc_ID']
            df_lemma['Dummy'] = df_doc['AC_Doc_ID']
            df_lemma_all = df_lemma_all.append(df_lemma)
            list_doc_id[i] = i
    else:
        for i, x in enumerate(list_cntnt):
            lemmas = []
            sentences = sent_detector.tokenize(x.strip())
            for y in sentences:
                tokens = nltk.word_tokenize(y)
                words = [w.lower() for w in tokens]
                lemmas_v = [wnl.lemmatize(t, 'v') for t in words]
                lemmas = lemmas + [wnl.lemmatize(t) for t in lemmas_v]
            
            s = ' '.join(lemmas)
            list_cntnt_lemma[i] = s
            print(s)
            df_lemma = pd.DataFrame({ 'Lemma' : lemmas })
            df_doc = pd.DataFrame({ 'AC_Doc_ID' : np.array([i] * len(df_lemma)) })
            df_lemma['AC_Doc_ID'] = df_doc['AC_Doc_ID']
            df_lemma['Dummy'] = df_doc['AC_Doc_ID']
            df_lemma_all = df_lemma_all.append(df_lemma)
            list_doc_id[i] = i

    df_doc_id = pd.DataFrame({ 'AC_Doc_ID' : list_doc_id })
    df_ac_buf['AC_Doc_ID'] = df_doc_id['AC_Doc_ID']
    df_cntnt_lemma = pd.DataFrame({ 'Cntnt_Lemma' : list_cntnt_lemma })
    df_ac_buf['Cntnt_Lemma'] = df_cntnt_lemma['Cntnt_Lemma']

    #Updated 1/16/2017 mack.sano@gmail.com
    if df_lemma_all.shape[0] > 0:
        #Updated 3/4/2017 mack.sano@gmail.com
        pd_ver = list(map(int, pd.__version__.split('.')))
        if (pd_ver[0] > 0) or (pd_ver[1] > 13):
            df_crosstab = df_lemma_all.pivot_table(values='Dummy', 
                index='AC_Doc_ID', columns='Lemma', aggfunc = len)
        else:
            df_crosstab = df_lemma_all.pivot_table(values='Dummy', 
                rows='AC_Doc_ID', cols='Lemma', aggfunc = len)
        df_crosstab['AC_Doc_ID'] = df_doc_id['AC_Doc_ID']
        df_res = pd.merge(df_ac_buf, df_crosstab, on='AC_Doc_ID')
    else:
        df_res = df_ac_buf

    return df_res.set_index('AC_Doc_ID')
