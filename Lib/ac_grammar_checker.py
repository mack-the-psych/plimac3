################################################################################
# This module parses and matches the text in the specified column of the input
# pandas.DataFrame for garammar check. The module recognizes each input record 
# as a unit of assessment content (i.e. a single passage section, an item stem,
# or an item option) and applies a serial number of 'AC_Doc_ID' to the each
# output record for the following processing.
# Parameters df_ac: input pandas.DataFrame, it should have, at least, one 
#                   column of text assessment content  
#            content_column: column name of text assessment content to be 
#                            parsed and matched
#            grammer: grammer for nltk.RegexpParser
#            grammar_check_label: specify the prefix of result columns
#            reg_exp_key=None: search key by a regular expression
# Returns Result: pandas.DataFrame including the original columns of the input 
#                 DataFrame plus parsed and matched result columns
################################################################################
def ac_grammar_checker(df_ac, content_column, grammer, grammar_check_label, 
        reg_exp_key=None):
    import pandas as pd
    import numpy as np
    import nltk
    import nltk.data
    import re

    wnl = nltk.WordNetLemmatizer()

    cp = nltk.RegexpParser(grammer, loop=2)
    sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')

    df_ac_buf = df_ac.copy()
    list_cntnt = list(df_ac_buf[content_column])
    list_cntnt_parsed = list_cntnt[:]
    list_doc_id = list_cntnt[:]    
    list_find_flg = list_cntnt[:]

    for i, x in enumerate(list_cntnt):
        chunks = []
        parsed = ''
        list_find_flg[i] = 0
        sentences = sent_detector.tokenize(x.strip())
        for y in sentences:
            tokens = nltk.word_tokenize(y)
            sentence_tkn = nltk.pos_tag(tokens)
            sentence_parsed = cp.parse(sentence_tkn)
            parsed = parsed + str(sentence_parsed) + ';'
            for v in sentence_parsed:
                is_gc_label = False
                if type(v) is nltk.Tree and v.label() == grammar_check_label:
                    is_gc_label = True
                if is_gc_label == True:
                    if len(v.leaves()) > 1:
                        chnk = ''
                        for j, w in enumerate(v.leaves()):
                            if j != 0:
                                chnk = chnk + ' '
                            chnk = chnk + w[0]
                        if reg_exp_key is None:
                            chunks = chunks + [chnk]
                            print('Grammar Check: ' + chnk)
                            list_find_flg[i] = list_find_flg[i] + 1
                        else:
                            if re.match(reg_exp_key, chnk) != None:
                                chunks = chunks + [chnk]
                                print('Grammar Check: ' + chnk)
                                list_find_flg[i] = list_find_flg[i] + 1

        list_doc_id[i] = i        
        list_cntnt_parsed[i] = parsed
        print(parsed)

    title_reg_exp_str = grammar_check_label + '_Cntnt'
    title_reg_exp_flg = grammar_check_label + '_Frq'

    df_doc_id = pd.DataFrame({ 'AC_Doc_ID' : list_doc_id })
    df_reg_flg = pd.DataFrame({ title_reg_exp_flg : list_find_flg })
    df_cntnt_find = pd.DataFrame({ title_reg_exp_str : list_cntnt_parsed })

    df_ac_buf['AC_Doc_ID'] = df_doc_id['AC_Doc_ID']
    df_ac_buf[title_reg_exp_str] = df_cntnt_find[title_reg_exp_str]
    df_ac_buf[title_reg_exp_flg] = df_reg_flg[title_reg_exp_flg]

    return df_ac_buf.set_index('AC_Doc_ID')
