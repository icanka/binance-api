#!/bin/python
import os
import sys
import time
from datetime import datetime

from binance.client import Client

TEST_NET_API_KEY = "p6ehIPJBn3O8BEPQWugN8H5MJmLNGIc2MyQQap87p8Y69ivr1ZT8QYlXYIveV6zP"
TEST_NET_API_SECRET = "arZLaiacx84Dx8gpc4bo4TtpHEsKhfeFlNk5ZvHtvDaA7UBxKpDkETygFyUlwAyC"


API_KEY = "pcCdG8wBaFv91qdTeAAnt3L4LRkXU4bNbIen8CSyZEZVrfevjonJWJpKpRGObgtG"
API_SECRET = "vyeaoz7MQv4Swp3kdArCHnZgbtLE9BH858UCIqdXuzRVs05ZmSL7ck3Z03cg3Hzh"
client = Client(TEST_NET_API_KEY, TEST_NET_API_SECRET, testnet=True)
# depth = client.get_order_book(symbol='BNBBTC')

# tickers = client.get_all_tickers()
# ticker = client.get_ticker(symbol='WINUSDT')
# price = client.get_avg_price(symbol="WINUSDT")
# info = client.get_account_snapshot(type='SPOT')


# klines = client.get_historical_klines("WINUSDT", Client.KLINE_INTERVAL_1MINUTE, '5 minutes ago UTC')
# volume = float(klines[0][5]) / 1000000

PARITY = sys.argv[1]
print(PARITY)

klines = client.get_historical_klines(
    PARITY, Client.KLINE_INTERVAL_1MINUTE, "60 minutes ago UTC"
)
avg_price = client.get_avg_price(symbol=PARITY)
ticker_price = client.get_symbol_ticker(symbol=PARITY)

DIVIDE = 0.0
DIVIDE_KLINE = 0.0
while True:
    klines.reverse()

    time.sleep(1)
    os.system("cls" if os.name == "nt" else "clear")

    avg_price = float(avg_price["price"])
    ticker_price = float(ticker_price["price"])

    TOTAL_AVG = 0.0
    FIRST = True
    for kline in klines:
        timestamp = int(kline[0]) / 1_000
        _open = float(kline[1])
        high = float(kline[2])
        low = float(kline[3])
        close = float(kline[4])
        avg = (_open + high + low + close) / 4
        TOTAL_AVG += avg
        date_hour = datetime.fromtimestamp(timestamp).strftime("%H:%M")
        volume = float(kline[5]) / 1_000_000
        quote_volume = float(kline[7])

        # print('Volume  ------  Time')

        if FIRST:
            diff = ticker_price - avg
            DIVIDE_KLINE = (diff / avg) * 100
            print(
                "{:<15} {:<15} {:<15} {:<15} {:<15} {:^6} {:^18} {:^8} {:^18} {:^18} {:^18}".format(
                    "average",
                    "open",
                    "high",
                    "LOW",
                    "close",
                    "VOLUME",
                    "QUOTE_VOLUME",
                    "DATE_HOUR",
                    "TICKER_PRICE",
                    "CHANGE_LAST_X_MIN",
                    "1MIN_AVG_CHANGE",
                )
            )
            print(
                "{:<15.6f} {:<15.6f} {:<15.6f} {:<15.6f} {:<15.6f} {:^6.2f} {:^18.0f} {:^8} {:^18.6f} {:^18.2f} {:^18.2f}".format(
                    avg,
                    _open,
                    high,
                    low,
                    close,
                    volume,
                    quote_volume,
                    date_hour,
                    ticker_price,
                    DIVIDE,
                    DIVIDE_KLINE,
                ),
                end="",
            )
            FIRST = False
        # else:
        # print('{:<12.6f} {:<12.6f} {:<12.6f} {:<12.6f} {:<12.6f} {:^6.2f} {:^10.0f} {:^5}'
        #       .format(avg, open, high, low, close, volume, quote_volume, date_hour), end='')

        # print()
    print()
    TOTAL_AVG /= len(klines)
    diff = ticker_price - TOTAL_AVG
    DIVIDE = (diff / TOTAL_AVG) * 100

    # print('{:<12.8f}'.format(total_avg))
    # print(avg_price)

    klines = client.get_historical_klines(
        PARITY, Client.KLINE_INTERVAL_1MINUTE, "60 minutes ago UTC"
    )
    avg_price = client.get_avg_price(symbol=PARITY)
    ticker_price = client.get_symbol_ticker(symbol=PARITY)
