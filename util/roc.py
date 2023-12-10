########################################
##### PANDAS  Rate Of Change(ROC)  #####
########################################

import pandas as pd
import numpy as np


def __ROC ( df, n=12, m=6, cl='Close' ):
    df['ROC']   = ( df[cl] - df[cl].shift(n))/df[cl].shift(n) * 100
    df['ROCMA'] = df["ROC"].rolling(m).mean()
    return df

