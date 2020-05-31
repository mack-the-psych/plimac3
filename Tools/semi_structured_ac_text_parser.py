###############################################################################
# This module is for generating a pandas.DataFrame from semi-structured 
# text data.
# Parameters file_name: string file path (input file),
#                       the input file is assumed, a) the first line contains 
#                       valid content to be parsed, b) the tags located the very 
#                       first column of each valid line
#            col_names: a list of tag names which will be applied as each
#                       column name of the DataFrame
#            lang = 'En' : Language option ('En' or 'Jp')
# Returns Result: pandas.DataFrame as a reformatted text data
################################################################################
def semi_structured_ac_text_parser(file_name, col_names,
                                   lang = 'En'):
    import sys
    import pandas as pd

    try:
        if lang == 'Jp':
            import codecs
            f = codecs.open(file_name,"r",'utf-8-sig')
        else:
            f = open(file_name, 'rU')
    except(Exception, e):
        print(e, 'error occurred')
        sys.exit()
    
    df_question = pd.DataFrame(columns=col_names)
    df_buf = pd.DataFrame.from_items([('0',col_names)],
                                    orient='index', columns=col_names)
    s_buf = ''
    num = 0
    latestNum = 0

    for line in f:
        res = line.find(col_names[num])
        if res == 0:
            if s_buf != '':
                print(str(latestNum) + ' ' + col_names[latestNum])
                print(s_buf)
                df_buf.iloc[0,latestNum] = s_buf.strip()
                s_buf = ''
                if num == 0:
                    df_question = df_question.append(df_buf)
            s_buf = line[len(col_names[num]):]
            latestNum = num
            if num < (len(col_names) - 1):
                num += 1
            else:
                num = 0
        else:
            s_buf += line

    f.close()

    if s_buf != '':
        print(str(latestNum) + ' ' + col_names[latestNum])
        print(s_buf)
        df_buf.iloc[0,latestNum] = s_buf.strip()
        s_buf = ''
        df_question = df_question.append(df_buf)

    df_question = df_question.set_index(col_names[0])
    
    return df_question
