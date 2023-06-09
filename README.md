# sta

```
$ python3 main.py --help
usage: main.py [-h] -i INTERVAL [-l LOGFILE] -t TICKERS [TICKERS ...] [-s STRATEGIES [STRATEGIES ...]] [-r REFRESH] [-p PERCENTAGE]

Script that monitors a number of tickers

options:
  -h, --help            show this help message and exit
  -i INTERVAL, --interval INTERVAL
                        time interval i.e. one of 1m, 5m, 15m, 30m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo
  -l LOGFILE, --logfile LOGFILE
                        log file i.e. app.log
  -t TICKERS [TICKERS ...], --tickers TICKERS [TICKERS ...]
                        list of stock tickers
  -s STRATEGIES [STRATEGIES ...], --strategies STRATEGIES [STRATEGIES ...]
                        load named strategies from strategie/ folder
  -r REFRESH, --refresh REFRESH
                        override default refresh settings, in seconds
  -p PERCENTAGE, --percentage PERCENTAGE
                        use strategies that return more than %



$ python3 main.py -i 1h -t AAPL SPY

-------------------------  1  -------------------------
=====  AAPL  =====  2023-04-25 11:52:26  =====
AAPL 1h ---> LONG ::: 27_MACDStrategy ::: (['CCI', 'MACD'],)
AAPL 1h ---> SHORT ::: 46_MQL5_elder_ray2 ::: (['EMA_13', 'EMA_21'],)


=====  SPY  =====  2023-04-25 11:52:40  =====
SPY 1h ---> SHORT ::: 113_EMA_TEMA ::: (['EMA_9', 'TEMA_30'],)
SPY 1h ---> SHORT ::: 46_MQL5_elder_ray2 ::: (['EMA_13', 'EMA_21'],)



$ python3 main.py -i 1h -l app.log --tickers AAPL SPY XLE --strategies 111_SMA_20_Close.py 113_EMA_TEMA.py 114_TSI.py 112_CCI_MFI_RSI_STO_WR.py
-------------------------  1  -------------------------
=====  AAPL  =====  2023-04-25 12:06:11  =====
=====  SPY  =====  2023-04-25 12:06:18  =====
SPY 1h ---> SHORT ::: 113_EMA_TEMA ::: (['EMA_9', 'TEMA_30'],)
=====  XLE  =====  2023-04-25 12:06:24  =====

```


### Completed
- [x] add indicators and oscillators
- [x] continuously run the program 
- [x] print initial matching strategies, after which print new matching strategies only


### TODO
- [ ] Add/fix plotting  for all strategies
- [ ] Add/fix benchmarks for add strategies

- [x] Add Discord/Slack text alerting
- [ ] Add Discord/Slack plotting for every matching strategy

- [ ] Add support for other data pandas/ohlc sources ( Alpaca, Alpha Vantage, Quandl )
- [ ] Add support for data sources ( TradingView, TD Ameritrade etc )

- [ ] Find more volunteers / contributors to this script
- [ ] Retire wealthy in 5 years :-P
