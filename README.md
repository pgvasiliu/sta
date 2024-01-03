# sta

### Description
This program pulls data from Yahoo finance and generates plots for each of the strategies listed in the
"strategies" folder ( i.e. 13 & 20 SMA cross, 9 & 21 EMA cross etc ). It also monitors tickers and
displays matching strategies based on price and indicator data ( i.e. ema, sma, tema, macd, tsi etc )  
and prints success rate of each strategy based on daily backtesting.


```
Windows setup
Download https://github.com/winpython/winpython/releases/download/6.0.20230219/Winpython64-3.10.10.0b2.exe
Unzip / Install the file to a folder
Grab the repository as zip file and uncompress under "scripts" folder ( WPy64-310110\scripts\project_x )
Run "WinPython Command Prompt" in WPy64-310110 folder
Run the code in that shell:
    cd project_x
    pip install -r requirements.txt
    python main.py -i 1d -t AAPL SPY 
```

```
$ mkdir project
$ cd project
$ python3 -m venv  env
$ git clone https://github.com/pgvasiliu/sta 
$ . env/bin/activate
$ pip3 config set global.trusted-host "pypi.org files.pythonhosted.org pypi.python.org" --trusted-host=pypi.python.org --trusted-host=pypi.org --trusted-host=files.pythonhosted.org
$ pip3 install -r requirements.txt
$ python3 main.py -i 1d -t AAPL SPY
$ deactivate

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


$ python3 main.py -t SPY MSFT -i 1d -p 60
-------------------------  1  -------------------------
=====  MSFT [ 371.6  0.2 % ]   =====  2024-01-03 13:21:57  =====
MSFT 1d ---> SHORT ::: bolinger_rsi_sma.py ::: return 107 ::: ['BB', 'RSI', 'SMA_13']
MSFT 1d ---> SHORT ::: dwma_20_close_cross.py ::: return 91 ::: ['DWMA_20', 'DWMA_50', 'DWMA_20_50_cross']
MSFT 1d ---> LONG_TREND ::: ema_144_169_sma_5.py ::: return 114 ::: ['EMA_144', 'EMA_169', 'SMA_5']
MSFT 1d ---> LONG ::: srsi_1.py ::: return 89 ::: ['SRSI']


Bear signals:
SMA_5_8_Signal:BEAR
MFI_Signal:BEAR


-------------------------  2  -------------------------
=====  SPY [ 470.37  -0.48 % ]   =====  2024-01-03 13:22:14  =====
SPY 1d ---> SHORT ::: adx_rsi ::: return 67 ::: ['ADX', 'RSI']





$ python3 main.py -i 1d -l app.log --tickers AAPL SPY XLE --strategies sma_13_close_cross.py sma_20_close_cross.py tsi_cross.py tema9_close_cross.py
-------------------------  1  -------------------------
=====  AAPL [ 184.45  -0.64 % ]   =====  2024-01-03 13:27:36  =====




-------------------------  2  -------------------------
=====  SPY [ 470.37  -0.48 % ]   =====  2024-01-03 13:27:41  =====


Bear signals:
STO_Signal:BEAR


-------------------------  3  -------------------------
=====  XLE [ 86.08  1.58 % ]   =====  2024-01-03 13:27:45  =====


Bull signals:
KDJ_Signal:BULL
Bear signals:
SMA_5_8_Signal:BEAR
```

```
Using tmux:
$ sudo dnf install tmux
$ git clone https://github.com/pgvasiliu/sta
$ cd sta
$ cp .tmux.conf ~/
$ tmux new -s STA
^b d ( disconnect from tmux session )

$ python3 work.py
$ tmux at

# Generate plots for a ticker
$ cd plotting; sh RUN.sh MFC.TO

Open your browser to <IP>:8000 to see plots and Tradingview graphs

```


### Completed
- [x] add indicators and oscillators
- [x] continuously run the program 
- [x] print initial matching strategies, after which print new matching strategies only


### TODO
- [x] Add/fix plotting  for all strategies
- [x] Add/fix benchmarks for add strategies

- [x] Add web interface to view png files / plots
- [x] Add Discord/Slack text alerting


### Images

![plots](https://github.com/pgvasiliu/sta/blob/main/_img/plots.png?raw=true)
![tradingview](https://github.com/pgvasiliu/sta/blob/main/_img/tradingview.png?raw=true)

