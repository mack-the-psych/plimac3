################################################################################
# The module reorders each row by the correlation value in descending order and 
# provides the reordered correlation values and the indices (reordered item IDs).
# Parameters df_ac: input pandas.DataFrame of correlation matrix as a result of 
#                   pandas.DataFrame.corr(), the module assumes there is no 
#                   'nan' value
#            index_name = 'INDEX': name of the index (item ID) matrix
#            value_name = 'VALUE': name of the correlation value matrix
# Returns Result: pandas.Panel as a result of reordered matrices (the indices 
# and correlation values respectively)
################################################################################
def ac_reorder_correlation_matrix(df_ac, index_name = 'INDEX', value_name = 'VALUE'):
    import pandas as pd

    df_ac_buf = df_ac[:]
    ac_buf_index = df_ac_buf.index

    df_buf_index = pd.DataFrame()
    df_buf_value = pd.DataFrame()

    for x in ac_buf_index:
        sr_q_x = df_ac_buf.xs(x)
        sr_q_x = sr_q_x.drop(x)
        sr_q_x = sr_q_x.sort_values(ascending=False)

        df_buf_index_x = pd.DataFrame(sr_q_x.index, index=range(1, (len(sr_q_x) + 1)), columns=[x])
        df_buf_value_x = pd.DataFrame(sr_q_x.values, index=range(1, (len(sr_q_x) + 1)), columns=[x])
        
        df_buf_index = df_buf_index.append(df_buf_index_x.transpose())
        df_buf_value = df_buf_value.append(df_buf_value_x.transpose())

    df_buf_index.index.name = index_name
    df_buf_value.index.name = value_name

    return pd.Panel({index_name : df_buf_index, value_name : df_buf_value})
