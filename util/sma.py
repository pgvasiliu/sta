########################
#####  PANDAS SMA  #####
########################

def __SMA ( data, n , cl='Close'):
    data['SMA_{}'.format(n)] = data[cl].rolling(window=n).mean()
    return data

