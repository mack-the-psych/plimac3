################################################################################
# This module is for replacing specified words in an input text file to 
#       the other words located specified positions of the input file.
# Parameters file_name_r: string file path (input file) 
#            file_name_w: string file path (output file)
#            words_replace_from: a list of words to be replaced
#            words_replace_to: a list of words as replacements
#            positions_where: a list of integer column numbers (starting from   
#                             zero) where the original words are located within  
#                             a single line, if the value is -1, all the words
#                             to be replaced no matter where the words are 
#                             located
#            lang = 'En'    : Language option ('En' or 'Jp')
# Output: a text file with replaced words
# Returns Result: None
################################################################################
def replace_where_for_ac_text_parser(file_name_r, file_name_w, 
                                     words_replace_from, words_replace_to, positions_where,
                                     lang = 'En'):
    try:
        if lang == 'Jp':
            import codecs
            f = codecs.open(file_name_r,"r",'utf-8-sig')
            w = codecs.open(file_name_w,"w",'utf-8-sig')
        else:
            f = open(file_name_r, 'rU')
            w = open(file_name_w, 'w')
    except Exception as e:
        print(e, 'error occurred')
    else:
        for line in f:
            for i, wd_frm in enumerate(words_replace_from):
                res = line.find(wd_frm)
                if res != -1:
                    if res == positions_where[i]:
                        line = line[: positions_where[i] ] + words_replace_to[i] + line[(positions_where[i] + len(words_replace_from[i])):]
                    else:
                        if positions_where[i] == -1:
                            line = line.replace(wd_frm, words_replace_to[i])
    
            w.write(line)
            print(line)
    finally:
        f.close()
        w.close()

    return
