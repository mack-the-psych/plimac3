################################################################################
# This module parses the text in the specified column of the input
# pandas.DataFrame for noun chunks. The module recognizes each input record as 
# a unit of assessment content (i.e. a single passage section, an item stem, 
# or an item option) and applies a serial number of 'AC_Doc_ID' to the each
# output record for the following processing.
# Parameters df_ac: input pandas.DataFrame, it should have, at least, one 
#                   column of text assessment content  
#            content_column: column name of text assessment content to be 
#                            parsed
#            grammer: grammer for nltk.RegexpParser
#            lang = 'En' : Language option ('En' or 'Jp')
# Returns Result: pandas.DataFrame including the original columns of the input 
#                 DataFrame plus parsed result columns
################################################################################
def ac_regexp_parser(df_ac, content_column, grammer, lang = 'En'):
    import pandas as pd
    import numpy as np
    import nltk
    import re
    #import sys
    #reload(sys)

    if lang == 'Jp':
        #sys.setdefaultencoding('utf-8')
        from janome.tokenizer import Tokenizer
        tagger = Tokenizer()
    else:
        wnl = nltk.WordNetLemmatizer()
        import nltk.data
        sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')

    cp = nltk.RegexpParser(grammer, loop=2)
    sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')

    df_ac_buf = df_ac.copy()
    list_cntnt = list(df_ac_buf[content_column])
    list_cntnt_parsed = list_cntnt[:]
    list_doc_id = list_cntnt[:]    
    df_nchunk_all = pd.DataFrame()

    if lang == 'Jp':
        for i, x in enumerate(list_cntnt):
            nchunks = []
            sentences = x.splitlines()
            for y in sentences:
                tagged = []
                for token in tagger.tokenize(y.strip()):
                    surface = token.surface
                    feature = token.part_of_speech
                    feature_list = feature.split(',')
                    tpl = surface, (feature_list[0] + '-' + feature_list[1])
                    tagged = tagged + [tpl]
                    
                if len(tagged) > 0:
                    parsed = cp.parse(tagged)
                    
                    nltk_ver = list(map(int, nltk.__version__.split('.')))
                    
                    for v in parsed:
                        if (nltk_ver[0] > 2):
                            if type(v) is nltk.Tree and v.label() == u'NCHUNK':
                                chnk = u''
                                for w in v.leaves():
                                    chnk = chnk + w[0]
                                nchunks = nchunks + [chnk]
                        else:
                            if type(v) is nltk.Tree and v.node == u'NCHUNK':
                                chnk = u''
                                for w in v.leaves():
                                    chnk = chnk + w[0]
                                nchunks = nchunks + [chnk]
                    
            s = ' '.join(nchunks)
            list_cntnt_parsed[i] = s
            print(s)

            df_nchunk = pd.DataFrame({ 'NP' : nchunks })
            df_doc = pd.DataFrame({ 'AC_Doc_ID' : np.array([i] * len(df_nchunk)) })
            df_nchunk['AC_Doc_ID'] = df_doc['AC_Doc_ID']
            df_nchunk['Dummy'] = df_doc['AC_Doc_ID']
            df_nchunk_all = df_nchunk_all.append(df_nchunk)
            list_doc_id[i] = i
    else:
        for i, x in enumerate(list_cntnt):
            nchunks = []
            parsed = ''
            sentences = sent_detector.tokenize(x.strip())
            for y in sentences:
                tokens = nltk.word_tokenize(y)
                #tagged = tagged + nltk.pos_tag(tokens)
                sentence_tkn = nltk.pos_tag(tokens)
                sentence_parsed = cp.parse(sentence_tkn)
                parsed = parsed + str(sentence_parsed) + ';'

                #Updated 3/5/2017 mack.sano@gmail.com
                nltk_ver = list(map(int, nltk.__version__.split('.')))
                
                for v in sentence_parsed:
                    #Updated 3/5/2017 mack.sano@gmail.com
                    is_nchunk = False
                    if (nltk_ver[0] > 2):
                        if type(v) is nltk.Tree and v.label() == u'NP':
                            is_nchunk = True
                    else:
                        if type(v) is nltk.Tree and v.node == u'NP':
                            is_nchunk = True
                    if is_nchunk == True and len(v.leaves()) > 1:
                        chnk = ''
                        for j, w in enumerate(v.leaves()):
                            if j != 0:
                                chnk = chnk + '_'
                            lemma = w[0].lower()
                            lemma = wnl.lemmatize(lemma, 'v')
                            lemma = wnl.lemmatize(lemma)
                            chnk = chnk + lemma
                        nchunks = nchunks + [chnk]
                               
            list_cntnt_parsed[i] = parsed
            print(parsed)

            df_nchunk = pd.DataFrame({ 'NP' : nchunks })
            df_doc = pd.DataFrame({ 'AC_Doc_ID' : np.array([i] * len(df_nchunk)) })
            df_nchunk['AC_Doc_ID'] = df_doc['AC_Doc_ID']
            df_nchunk['Dummy'] = df_doc['AC_Doc_ID']
            df_nchunk_all = df_nchunk_all.append(df_nchunk)
            list_doc_id[i] = i        

    df_doc_id = pd.DataFrame({ 'AC_Doc_ID' : list_doc_id })
    df_ac_buf['AC_Doc_ID'] = df_doc_id['AC_Doc_ID']
    df_cntnt_parsed = pd.DataFrame({ 'Cntnt_Parsed' : list_cntnt_parsed })
    df_ac_buf['Cntnt_Parsed'] = df_cntnt_parsed['Cntnt_Parsed']

    #Updated 11/13/2016 mack.sano@gmail.com
    if df_nchunk_all.shape[0] > 0:
        #Updated 3/5/2017 mack.sano@gmail.com
        pd_ver = list(map(int, pd.__version__.split('.')))
        if (pd_ver[0] > 0) or (pd_ver[1] > 13):
            df_crosstab = df_nchunk_all.pivot_table(values='Dummy', 
                index='AC_Doc_ID', columns='NP', aggfunc = len)
        else:
            df_crosstab = df_nchunk_all.pivot_table(values='Dummy', 
                rows='AC_Doc_ID', cols='NP', aggfunc = len)
            
        df_crosstab['AC_Doc_ID'] = df_doc_id['AC_Doc_ID']
        df_res = pd.merge(df_ac_buf, df_crosstab, on='AC_Doc_ID', how='left')
    else:
        df_res = df_ac_buf

    return df_res.set_index('AC_Doc_ID')
    
