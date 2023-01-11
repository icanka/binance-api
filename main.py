# This is a sample Python script.
import os
import time
from pprint import pprint
from binance.client import Client

TEST_NET_API_KEY = "Esnf1IZgyMIX5mQtYBWln1enlwgRhR41Z4W0E7GhEtrB7OLgRvOmGGggVAPg7uvE"
TEST_NET_API_SECRET = "m1labgzYW90jVJk56Y9Yn5aADyFB02gHmYtfpKk0m5EXOpQQcMTez82VdRFpbXz0"


API_KEY = "pcCdG8wBaFv91qdTeAAnt3L4LRkXU4bNbIen8CSyZEZVrfevjonJWJpKpRGObgtG"
API_SECRET = "vyeaoz7MQv4Swp3kdArCHnZgbtLE9BH858UCIqdXuzRVs05ZmSL7ck3Z03cg3Hzh"



# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    client = Client(TEST_NET_API_KEY, TEST_NET_API_SECRET, testnet=True)
    #depth = client.get_order_book(symbol='BNBBTC')
    #tickers = client.get_all_tickers()
    ticker = client.get_ticker(symbol='BTCBUSD')
    #pprint(ticker)
    price = client.get_avg_price(symbol="BTCBUSD")
    #info = client.get_account_snapshot(type='FUTURES')
    test = client.get_asset_balance(asset="BUSD")
    pprint(test)
    # orders = client.get_all_orders(symbol="BTCBUSD")
    order = client.order_market_buy(
    symbol='BTCBUSD',
    quantity='0.001')
    pprint(order)
    # client.futures_account_balance()
    # client.futures_account()
    # client.futures_account_trades()
    # client.futures_get_all_orders()
    # pprint(order)
    # while(True):
    #     time.sleep(0.1)
    #     #price = client.get_avg_price(symbol='BTCBUSD')
    #     price = client.get_symbol_ticker(symbol='BTCBUSD')
    #     #os.system('cls' if os.name == 'nt' else 'clear')
    #     pprint(price['price'])
    #pprint(ticker)
    #pprint(price)
    #pprint(prices)
    #pprint(tickers)
    #print(tickers[0]['price'])




# See PyCharm help at https://www.jetbrains.com/help/pycharm/
