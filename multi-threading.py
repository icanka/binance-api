import threading
import os
import sys
import time
from datetime import datetime
from binance.client import Client

def get_market_data(symbol):
    """
    function to print cube of given num
    """
    api_key = "ozlwREBYvQmm0TGorxEMxXUbw72GBCwbTG8k7XgmD7DcL0IPvrt9DGlfDY36tNmm"
    api_secret = "9PHbVFlWJ4ohNjSePs7SWxHorovrf3kFLhu1OdSpgAEBWlDmPZREfLrDgITByS35"
    client = Client(api_key, api_secret)
    ticker_price = client.get_symbol_ticker(symbol=symbol)
    print(ticker_price)



if __name__ == "__main__":
    # creating thread
    symbol="WINUSDT"
    t1 = threading.Thread(target=get_market_data, args=(symbol,))

    # starting thread 1
    t1.start()
    # starting thread 2
    #t2.start()

    # wait until thread 1 is completely executed
    t1.join()
    # wait until thread 2 is completely executed
    #t2.join()

    # both threads completely executed
    print("Done!")