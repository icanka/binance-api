#!/bin/python
import os
import sys
import time
from datetime import datetime

from binance.client import Client

api_key = "ozlwREBYvQmm0TGorxEMxXUbw72GBCwbTG8k7XgmD7DcL0IPvrt9DGlfDY36tNmm"
api_secret = "9PHbVFlWJ4ohNjSePs7SWxHorovrf3kFLhu1OdSpgAEBWlDmPZREfLrDgITByS35"
client = Client(api_key, api_secret)
# depth = client.get_order_book(symbol='BNBBTC')

# tickers = client.get_all_tickers()
# ticker = client.get_ticker(symbol='WINUSDT')
# price = client.get_avg_price(symbol="WINUSDT")
# info = client.get_account_snapshot(type='SPOT')


# klines = client.get_historical_klines("WINUSDT", Client.KLINE_INTERVAL_1MINUTE, '5 minutes ago UTC')
# volume = float(klines[0][5]) / 1000000

parite = sys.argv[1]
print(parite)

klines = client.get_historical_klines(parite, Client.KLINE_INTERVAL_1DAY, '3 months ago UTC')
avg_price = client.get_avg_price(symbol=parite)
ticker_price = client.get_symbol_ticker(symbol=parite)

divide = 0.0
divide_kline = 0.0
while True:
    klines.reverse()

    time.sleep(1)
    os.system('cls' if os.name == 'nt' else 'clear')

    avg_price = float(avg_price['price'])
    ticker_price = float(ticker_price['price'])

    total_avg = 0.0
    first = True
    for kline in klines:
        timestamp = int(kline[0]) / 1_000
        open = float(kline[1])
        high = float(kline[2])
        low = float(kline[3])
        close = float(kline[4])
        avg = (open + high + low + close) / 4
        total_avg += avg
        date_hour = datetime.fromtimestamp(timestamp).strftime('%H:%M')
        volume = float(kline[5]) / 1_000_000
        quote_volume = float(kline[7])

        # print('Volume  ------  Time')

        if first:
            diff = ticker_price - avg
            divide_kline = (diff / avg) * 100
            print('{:<12} {:<12} {:<12} {:<12} {:<12} {:^6} {:^18} {:^8} {:^18} {:^18} {:^18}'.
                  format('average', 'open', 'high', 'LOW', 'close', 'VOLUME', 'QUOTE_VOLUME', 'DATE_HOUR', 'TICKER_PRICE', 'CHANGE_LAST_X_MIN', '1MIN_AVG_CHANGE'))
            print(
                '{:<12.6f} {:<12.6f} {:<12.6f} {:<12.6f} {:<12.6f} {:^6.2f} {:^18.0f} {:^8} {:^18.6f} {:^18.2f} {:^18.2f}'
                    .format(avg, open, high, low, close, volume, quote_volume, date_hour, ticker_price, divide,
                            divide_kline), end='')
            first = False
        # else:
        # print('{:<12.6f} {:<12.6f} {:<12.6f} {:<12.6f} {:<12.6f} {:^6.2f} {:^10.0f} {:^5}'
        #       .format(avg, open, high, low, close, volume, quote_volume, date_hour), end='')

        #print()
    print()
    total_avg /= len(klines)
    diff = ticker_price - total_avg
    divide = (diff / total_avg) * 100

    # print('{:<12.8f}'.format(total_avg))
    # print(avg_price)

    klines = client.get_historical_klines(parite, Client.KLINE_INTERVAL_1DAY, '3 months ago UTC')
    avg_price = client.get_avg_price(symbol=parite)
    ticker_price = client.get_symbol_ticker(symbol=parite)
