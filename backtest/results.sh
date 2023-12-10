#!/bin/bash

mkdir -p results


GREEN=$(tput setaf 2)
NORMAL=$(tput sgr0)

#for i in AAPL CROX MSFT NVDA SHOP SPY TSLA TD.TO BMO.TO OVV.TO SLF.TO GWO.TO BNS.TO RY.TO
#for i in AAPL CROX MSFT NVDA SHOP SPY TSLA XHB XLC XLE XLF XLI XLK XLU XLV XLY XME XRT XTN
for i in OVV.TO TD.TO BNS.TO GWO.TO MFC.TO SLF.TO
do
    rm -f results/$i ../data/$i*csv
    for x in `ls -1 *py | egrep -vE "(X|stats)"`
    do
        echo
        echo " --->>>  Exec [${GREEN}$x -t $i -l results/$i${NORMAL}]"
        python3 $x -t $i -l results/$i
        #sleep 1
    done
    cat results/$i | sort -nr -k 3 | tee results/$i.tmp
    mv -f results/$i.tmp results/$i

    git add results/$i
    git commit -m "$i results folder updates"
    git push
done


