################################################################################
# This module processes the text in the specified column of the input
# pandas.DataFrame for n-grams. The module recognizes each input record as 
# a unit of assessment content (i.e. a single passage section, an item stem, 
# or an item option) and applies a serial number of 'AC_Doc_ID' to the each
# output record for the following processing.
# Parameters df_ac: input pandas.DataFrame, it should have, at least, one 
#                   column of text assessment content
#            content_column: column name of text assessment content for n-grams
#            gram = 'bigram': specify bigram or trigram
#            lang = 'En' : Language option ('En' or 'Jp')
# Returns Result: pandas.DataFrame including the original columns of the input 
#                 DataFrame plus n-gram result columns
################################################################################
def ac_bi_trigram(df_ac, content_column, gram = 'bigram', lang = 'En'):
    import pandas as pd
    import numpy as np
    import nltk

    if lang == 'Jp':
        from janome.tokenizer import Tokenizer
        tagger = Tokenizer()
    else:
        wnl = nltk.WordNetLemmatizer()
        import nltk.data
        sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    
    df_ac_buf = df_ac.copy()
    list_cntnt = list(df_ac_buf[content_column])
    list_cntnt_ngram = list_cntnt[:]
    list_doc_id = list_cntnt[:]
    df_ngram_all = pd.DataFrame()

    for i, x in enumerate(list_cntnt):
        ngram = []
        if lang == 'Jp':
            sentences = x.splitlines()
            for y in sentences:
                lemmas = []
                for token in tagger.tokenize(y.strip()):
                    surface = token.surface
                    feature = token.part_of_speech
                    feature_list = feature.split(',')
                    if surface != u' ':
                        if token.base_form != u'*':
                            lemmas = lemmas + [token.base_form]
                        else:
                            lemmas = lemmas + [surface]
                            
                #Updated 3/5/2017 mack.sano@gmail.com
                if gram == 'bigram':
                    ngram = ngram + list(nltk.bigrams(lemmas))
                else:
                    ngram = ngram + list(nltk.trigrams(lemmas))
        else:
            sentences = sent_detector.tokenize(x.strip())
            for y in sentences:
                lemmas = []
                tokens = nltk.word_tokenize(y)
                words = [w.lower() for w in tokens]
                lemmas_v = [wnl.lemmatize(t, 'v') for t in words]
                lemmas = lemmas + [wnl.lemmatize(t) for t in lemmas_v]

                #Updated 3/5/2017 mack.sano@gmail.com
                if gram == 'bigram':
                    ngram = ngram + list(nltk.bigrams(lemmas))
                else:
                    ngram = ngram + list(nltk.trigrams(lemmas))

        if len(ngram) == 0:
            str_ngram = ''
        else:
            str_ngram = str(ngram)
        
        if lang == 'Jp':
            list_cntnt_ngram[i] = pp(str_ngram)
        else:
            list_cntnt_ngram[i] = str_ngram
        print(list_cntnt_ngram[i])

        list_ngrams = []
        
        for v in ngram:
            cmbnd_ngram = ''
            for j, w in enumerate(v):
                if j != 0:
                    cmbnd_ngram = cmbnd_ngram + '_'
                cmbnd_ngram = cmbnd_ngram + w
            list_ngrams = list_ngrams + [cmbnd_ngram]

        df_ngram = pd.DataFrame({ 'NGrams' : list_ngrams })
        df_doc = pd.DataFrame({ 'AC_Doc_ID' : np.array([i] * len(df_ngram)) })
        df_ngram['AC_Doc_ID'] = df_doc['AC_Doc_ID']
        df_ngram['Dummy'] = df_doc['AC_Doc_ID']
        df_ngram_all = df_ngram_all.append(df_ngram)
        list_doc_id[i] = i        

    df_doc_id = pd.DataFrame({ 'AC_Doc_ID' : list_doc_id })
    df_ac_buf['AC_Doc_ID'] = df_doc_id['AC_Doc_ID']
    if gram == 'bigram':
        title_ngram = 'Cntnt_Bigram'
    else:
        title_ngram = 'Cntnt_Trigram'
    
    df_cntnt_parsed = pd.DataFrame({ title_ngram : list_cntnt_ngram })
    df_ac_buf[title_ngram] = df_cntnt_parsed[title_ngram]

    #Updated 11/13/2016 mack.sano@gmail.com
    if df_ngram_all.shape[0] > 0:
        #Updated 3/5/2017 mack.sano@gmail.com
        pd_ver = list(map(int, pd.__version__.split('.')))
        if (pd_ver[0] > 0) or (pd_ver[1] > 13):
            df_crosstab = df_ngram_all.pivot_table(values='Dummy', 
                    index='AC_Doc_ID', columns='NGrams', aggfunc = len)
        else:
            df_crosstab = df_ngram_all.pivot_table(values='Dummy', 
                    rows='AC_Doc_ID', cols='NGrams', aggfunc = len)
        df_crosstab['AC_Doc_ID'] = df_doc_id['AC_Doc_ID']
        df_res = pd.merge(df_ac_buf, df_crosstab, on='AC_Doc_ID', how='left')
    else:
        df_res = df_ac_buf

    return df_res.set_index('AC_Doc_ID')

# from http://nltk.googlecode.com/svn/trunk/doc/book-jp/ch12.html#id3
import re, pprint
def pp(obj):
    pp = pprint.PrettyPrinter(indent=4, width=160)
    str = pp.pformat(obj)
    return re.sub(r"\\u([0-9a-f]{4})", lambda x: unichr(int("0x"+x.group(1),
                                                            16)), str)
