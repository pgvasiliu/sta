#####  (10)  KDJ  #####
# KDJ CROSS  https://github.com/pgvasiliu/futu_algo/blob/master/strategies/KDJ_Cross.py
# You get a buy signal from the KDJ indicator when the three curves converge. 
# The blue K line crosses the D line from bottom to top and then moves above the yellow J line. The purple D line is at the bottom.
# The signal is even stronger when the golden form appears under the 20 line, that is in the oversold area.


data = __KDJ ( data )


if ( 20 > data['KDJ_D'][-1] > data['KDJ_D'][-2] > data['KDJ_K'][-2] )  &  ( data['KDJ_K'][-1] > data['KDJ_K'][-2] )  &  ( data['KDJ_K'][-1] > data['KDJ_D'][-1] ):
    print_log ( '6_KDJ', 'LONG', [ 'KDJ', 'KDJ_CROSSOVER' ] )

#A sell signal is received when the lines converge in a way that the blue line K crosses the line D from top to bottom. The blue line continues below the yellow and the purple one runs above the others.
#The signal is stronger when the dead fork of the KDJ oscillator occurs in the overbought zone that is above the line of 80 value.
if ( 80 < data['KDJ_D'][-1] < data['KDJ_D'][-2] < data['KDJ_K'][-2] ) and ( data['KDJ_K'][-1] < data['KDJ_K'][-2] ) and ( data['KDJ_K'][-1] < data['KDJ_D'][-1] ):
    print_log ( '6_KDJ', 'SHORT', [ 'KDJ', 'KDJ_CROSSOVER' ] )

