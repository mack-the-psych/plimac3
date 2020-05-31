################################################################################
# This module is for reformatting (serializing) a pandas.DataFrame which has
# item stem and corresponded answer options in one record for each question,  
# the module separates them into a single record per stem/option with repetitive 
# imputations of all the other column information originally assigned to the 
# question.
# Parameters file_name: CSV file path (input file)
#            id_column: question id column name
#            ser_columns: column names to be serialized
#            lang = 'En' : Language option ('En' or 'Jp')
# Returns Result: pandas.DataFrame as a serialized question data
################################################################################
def ac_column_serializer(file_name, id_column, ser_columns, lang = 'En'):
    import sys
    import pandas as pd
    import numpy as np

    try:
        if lang == 'Jp':
            df_all_input = pd.read_csv(file_name, encoding='utf-8')
        else:
            df_all_input = pd.read_csv(file_name)
    except Exception as e:
        print(e, 'error occurred')
        sys.exit()

    df_no_ser = df_all_input.copy()
    df_no_ser = df_no_ser.drop(ser_columns, axis=1)
    df_ser = pd.DataFrame()

    list_index = list(df_all_input[id_column])

    for i, index_value in enumerate(list_index):
        df_index = pd.DataFrame({ id_column : np.array([index_value] *
                                                         len(ser_columns)) })
        df_content = pd.DataFrame.from_items([('Pre_Col_Name', ser_columns),
                                             ('Content', ser_columns)])
        df_content[id_column] = df_index[id_column]
        for j, x in enumerate(ser_columns):
            df_content.loc[j, 'Content'] = df_all_input.loc[i, x]

        '''
        if lang == 'Jp':
            print(str(df_content).decode('utf8'))
        else:
            print(df_content)
        '''
        print(df_content)

        df_ser = df_ser.append(df_content)

    df_res = pd.merge(df_no_ser, df_ser, on=id_column)
    df_res = df_res.set_index(id_column)

    return df_res
