#!/bin/python
import os
import time

from binance.client import Client

api_key = "ozlwREBYvQmm0TGorxEMxXUbw72GBCwbTG8k7XgmD7DcL0IPvrt9DGlfDY36tNmm"
api_secret = "9PHbVFlWJ4ohNjSePs7SWxHorovrf3kFLhu1OdSpgAEBWlDmPZREfLrDgITByS35"
client = Client(api_key, api_secret)
# depth = client.get_order_book(symbol='BNBBTC')

# tickers = client.get_all_tickers()
# ticker = client.get_ticker(symbol='WINUSDT')
# price = client.get_avg_price(symbol="WINUSDT")
# info = client.get_account_snapshot(type='SPOT')

old_avg_price = 0
old_avg_tick = 0
old_divide = 0

while (True):
    time.sleep(0.1)
    os.system('cls' if os.name == 'nt' else 'clear')
    print('{0:10.8f} ---- {1:10.8f} ---- %{2:3.2f}'.format(old_avg_price, old_avg_tick, old_divide))



    avg_price = client.get_avg_price(symbol='WINUSDT')
    avg_price = float(avg_price['price'])
    ticker_price = client.get_symbol_ticker(symbol='WINUSDT')
    ticker_price = float(ticker_price['price'])


    diff = ticker_price - avg_price
    divide = (diff / avg_price) * 100

    old_avg_tick = ticker_price
    old_avg_price = avg_price
    old_divide = divide
