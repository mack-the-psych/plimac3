################################################################################
# This module tokenizes the text in the specified column of the input
# pandas.DataFrame and give part-of-speech tags to the tokens. The module  
# recognizes each input record as a unit of assessment content (i.e. a single  
# passage section, an item stem, or an item option) and applies a serial  
# number of 'AC_Doc_ID' to the each output record for the following processing.
# Parameters df_ac: input pandas.DataFrame, it should have, at least, one 
#                   column of text assessment content  
#            content_column: column name of text assessment content to be 
#                            tokenized and tagged
#            lang = 'En' : Language option ('En' or 'Jp')
# Returns Result: pandas.DataFrame including the original columns of the input 
#                 DataFrame plus tagged result columns
################################################################################
def ac_pos_tagger(df_ac, content_column, lang = 'En'):
    import pandas as pd
    import numpy as np

    if lang == 'Jp':
        from janome.tokenizer import Tokenizer
        tagger = Tokenizer()
    else:
        import nltk
        import nltk.data
        sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')

    df_ac_buf = df_ac.copy()
    list_cntnt = list(df_ac_buf[content_column])
    list_cntnt_pos = list_cntnt[:]
    list_doc_id = list_cntnt[:]    
    df_pos_all = pd.DataFrame()

    if lang == 'Jp':
        for i, x in enumerate(list_cntnt):
            tagged = []
            sentences = x.splitlines()
            for y in sentences:
                for token in tagger.tokenize(y.strip()):
                    surface = token.surface
                    feature = token.part_of_speech
                    feature_list = feature.split(',')
                    tpl = surface, (feature_list[0] + '-' + feature_list[1])
                    tagged = tagged + [tpl]
            
            df_pos = pd.DataFrame(tagged, columns=['Token', 'POS'])
            df_doc = pd.DataFrame({ 'AC_Doc_ID' : np.array([i] * len(df_pos)) })
            df_pos['AC_Doc_ID'] = df_doc['AC_Doc_ID']
            df_pos_all = df_pos_all.append(df_pos)
            list_cntnt_pos[i] = pp(str(tagged))
            print(list_cntnt_pos[i])
            list_doc_id[i] = i        
    else:
        for i, x in enumerate(list_cntnt):
            tagged = []
            sentences = sent_detector.tokenize(x.strip())
            for y in sentences:
                tokens = nltk.word_tokenize(y)
                tagged = tagged + nltk.pos_tag(tokens)
            
            df_pos = pd.DataFrame(tagged, columns=['Token', 'POS'])
            df_doc = pd.DataFrame({ 'AC_Doc_ID' : np.array([i] * len(df_pos)) })
            df_pos['AC_Doc_ID'] = df_doc['AC_Doc_ID']
            df_pos_all = df_pos_all.append(df_pos)
            list_cntnt_pos[i] = str(tagged)
            list_doc_id[i] = i        
            print(tagged)

    df_doc_id = pd.DataFrame({ 'AC_Doc_ID' : list_doc_id })
    df_ac_buf['AC_Doc_ID'] = df_doc_id['AC_Doc_ID']
    df_cntnt_pos = pd.DataFrame({ 'Cntnt_POS' : list_cntnt_pos })
    df_ac_buf['Cntnt_POS'] = df_cntnt_pos['Cntnt_POS']

    #Updated 1/16/2017 mack.sano@gmail.com
    if df_pos_all.shape[0] > 0:
        #Updated 3/4/2017 mack.sano@gmail.com
        pd_ver = list(map(int, pd.__version__.split('.')))
        if (pd_ver[0] > 0) or (pd_ver[1] > 13):
            df_crosstab = df_pos_all.pivot_table(values='Token', 
                index='AC_Doc_ID', columns='POS', aggfunc = len)

        else:
            df_crosstab = df_pos_all.pivot_table(values='Token', 
                rows='AC_Doc_ID', cols='POS', aggfunc = len)
        df_crosstab['AC_Doc_ID'] = df_doc_id['AC_Doc_ID']
        df_res = pd.merge(df_ac_buf, df_crosstab, on='AC_Doc_ID')
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
