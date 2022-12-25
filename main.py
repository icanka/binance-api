# This is a sample Python script.
import os
import time
from pprint import pprint
from binance.client import Client

api_key = "ozlwREBYvQmm0TGorxEMxXUbw72GBCwbTG8k7XgmD7DcL0IPvrt9DGlfDY36tNmm"
api_secret = "9PHbVFlWJ4ohNjSePs7SWxHorovrf3kFLhu1OdSpgAEBWlDmPZREfLrDgITByS35"



# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    client = Client(api_key, api_secret)
    #depth = client.get_order_book(symbol='BNBBTC')
    tickers = client.get_all_tickers()
    ticker = client.get_ticker(symbol='WINUSDT')
    price = client.get_avg_price(symbol="WINUSDT")
    info = client.get_account_snapshot(type='SPOT')
    while(True):
        time.sleep(0.1)
        price = client.get_avg_price(symbol='WINUSDT')
        pprint(price['price'])
        os.system('cls' if os.name == 'nt' else 'clear')
    #pprint(ticker)
    #pprint(price)
    #pprint(prices)
    #pprint(tickers)
    #print(tickers[0]['price'])




# See PyCharm help at https://www.jetbrains.com/help/pycharm/
