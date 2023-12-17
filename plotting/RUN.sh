#!/bin/sh

#rm -f ../data/*csv

TICKERS="SLF.TO GWO.TO TD.TO MFC.TO IMO.TO AAPL MSFT SPY NVDA IWM IJR APA XLE"
#TICKERS="GWO.TO"
for ticker in $TICKERS
do
    for i in $(ls -1 *py)
    do
	if [ ! -x $i ]
	then
            echo
            echo "========  $ticker - $i  ========"
            python3 $i -t $ticker -i 1d -c ../data/${ticker}_1d.csv
            python3 $i -t $ticker -i 1wk -c ../data/${ticker}_1wk.csv
            #sleep 2
        fi
    done
done
