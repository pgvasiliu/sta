##################################################
#####  PANDAS  Rolling Moving Average (RMA)  #####
##################################################
def __RMA(close, t):
    rma = []
    sma = SMA(close, t)
    for i in range(t):
        rma.append(sma[i])
    for i in range(t, len(close)):
        rma.append( (rma[i-1]*(t-1) + close[i])/t )
    return rma
# RMA Ends here

#def get_rma(interval,signal=False):
#    """
#    Media movil exponencial.
#    """
#    if type(signal)==bool:
#        signal=Close
#
#    rma=signal.ewm(alpha=1/interval,min_periods=interval).mean()#rma
#return rma

