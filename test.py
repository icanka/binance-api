#!/bin/python
from concurrent.futures import ProcessPoolExecutor as PoolExecutor
import threading
from datetime import datetime
from pprint import pprint

from binance.client import Client

api_key = "ozlwREBYvQmm0TGorxEMxXUbw72GBCwbTG8k7XgmD7DcL0IPvrt9DGlfDY36tNmm"
api_secret = "9PHbVFlWJ4ohNjSePs7SWxHorovrf3kFLhu1OdSpgAEBWlDmPZREfLrDgITByS35"
client = Client(api_key, api_secret)
# depth = client.get_order_book(symbol='BNBBTC')

tickers = client.get_ticker()

count = 0
for ticker in tickers:
    count += 1
    if ticker['symbol'].endswith('USDT') :
        print(ticker['symbol'])

print(count)


# tickers = client.get_all_tickers()
# ticker = client.get_ticker(symbol='WINUSDT')
# price = client.get_avg_price(symbol="WINUSDT")
# info = client.get_account_snapshot(type='SPOT')


# klines = client.get_historical_klines("WINUSDT", Client.KLINE_INTERVAL_1MINUTE, '5 minutes ago UTC')
# volume = float(klines[0][5]) / 1000000

pariteler = ['WINUSDT', 'VETUSDT', 'HOTUSDT']



#
# while True:
#     time.sleep(1)
#     os.system('cls' if os.name == 'nt' else 'clear')
#     print('{:<12} {:<12} {:<12} {:<12}'.format('average', 'open', 'high', 'close'))


# def binance(parite):
#     print(parite)
#     klines = client.get_historical_klines(parite, Client.KLINE_INTERVAL_1MINUTE, '15 minutes ago UTC')
#     print(type(klines))
#
# with PoolExecutor(max_workers=4) as executor:
#     for _ in executor.map(binance, pariteler):
#         pass
#

# pprint(klines)
# print(len(klines))
# print(len(klines[0]))
# pprint(volume)
# print(type(klines))
# pprint(klines[0][0])
# print(datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S'))
# print(datetime.utcfromtimestamp(timestamp).strftime('%H:%M'))
# print(datetime.fromtimestamp(timestamp).strftime('%H:%M'))

# dt_object = datetime.fromtimestamp(timestamp)
# print(dt_object)
# while (True):
#     os.system('cls' if os.name == 'nt' else 'clear')
#     print('{0:10.8f} ---- {1:10.8f} ---- %{2:3.2f}'.format(old_avg_price, old_avg_tick,old_divide))
#
#     time.sleep(1)
#
#
#     avg_price = client.get_avg_price(symbol='WINUSDT')
#     avg_price = float(avg_price['price'])
#     ticker_price = client.get_symbol_ticker(symbol='WINUSDT')
#     ticker_price = float(ticker_price['price'])
#     #avg_tick = float(ticker_price['bidPrice']) + float(ticker_price['askPrice'])
#     #avg_tick /= 2
#
#     diff = ticker_price - avg_price
#     divide = (diff/avg_price) * 100
#
#     old_avg_tick = ticker_price
#     old_avg_price = avg_price
#     old_divide = divide
#     #print('{0:10.8f}    {1:3f}'.format(diff, divide))
#
#     #avg_tick = round(avg_tick, 8)
#     #print('----avg_price----                        ----avg_tick----')
#
#
#     #print(avg_tick)
#     #print(avg_price['price'])
#     # os.system('cls' if os.name == 'nt' else 'clear')
