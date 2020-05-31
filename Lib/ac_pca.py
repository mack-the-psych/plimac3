################################################################################
# This module perform principal component analysis (PCA).
# Parameters df_ac: input pandas.DataFrame, it should have all numeric values  
#            feature_value_labels = None: labes of the numeric valuables
# Returns Result: pandas.DataFrame including the componet loadings and 
#                 eigen values of the PCA result
################################################################################
def ac_pca(df_ac, feature_value_labels = None):
    import pandas as pd
    import numpy as np
    import scipy
    from scipy import linalg

    df_ac_buf = df_ac.copy()

    data = df_ac_buf.values

    U, s, V = scipy.linalg.svd(np.corrcoef(data.transpose()))
    print(s)

    df_res = pd.DataFrame(np.array(V), index = range(1, (len(s) + 1)), columns=df_ac_buf.columns)
    df_res = (df_res.transpose() * (np.array(s) ** 0.5)).transpose()
    df_s = pd.DataFrame({ 'EIGEN_VALUES' : np.array(s) }, index = range(1, (len(s) + 1)))

    if feature_value_labels is not None:
        df_res.columns = feature_value_labels

    df_res['EIGEN_VALUES'] = df_s['EIGEN_VALUES']
    
    df_res = df_res.transpose()
    df_res.index.name = 'COMPONENT'

    return df_res
