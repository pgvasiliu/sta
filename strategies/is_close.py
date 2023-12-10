
current_price = data['Adj Close'][-1]

ma_200 = data['SMA_200'][-1]
#data['SMA200_Close_Signal'] = 0

# Check if the current price is within 2% of the 200-day MA
if current_price >= ma_200 * 0.98 and current_price <= ma_200 * 1.02:
    #data['SMA200_Close_Signal'] = 1
    print_log ( 'is_close.py', 'NEUTRAL', [ 'Adj Close', 'SMA_200' ] )


ma_50 = data['SMA_50'][-1]
#data['SMA50_Close_Signal'] = 0

if current_price >= ma_50 * 0.98 and current_price <= ma_50 * 1.02:
    #data['SMA50_Close_Signal'] = 1
    print_log ( 'is_close.py', 'NEUTRAL', [ 'Adj Close', 'SMA_50' ] )
