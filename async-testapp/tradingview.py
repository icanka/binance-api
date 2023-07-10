import asyncio
import datetime
import json
import random
import aiofiles
import requests as requests_sync
import requests_async as requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from bnc2 import get_ticker, calc_volume
from binance import AsyncClient
from binance.exceptions import BinanceAPIException
from pprint import pprint
from trview.config import DevelopmentConfig
from trview.models import Trview_recommend, Symbol24_h_volume


def get_symbols(screener_country):
    headers = {"User-Agent": "Mozilla/5.0"}
    url = "https://scanner.tradingview.com/{}/scan".format(screener_country)
    symbol_lists = requests_sync.post(url, headers=headers, timeout=10).json()
    data = symbol_lists["data"]
    for pair in data:
        data = pair["s"].split(":")
        _dict = {"symbol": data[1], "market": data[0]}
        yield _dict


async def get_ticker_price(symbol):
    client = await AsyncClient.create()
    try:
        pprint("req+")
        res = await client.get_ticker(symbol=symbol)
    except BinanceAPIException:
        pprint(f"Error getting ticker for {symbol}")
        await client.close_connection()
        pprint(f"Connection closed for {symbol}")
        raise
    finally:
        await client.close_connection()
    return res["lastPrice"]


async def get_signal(screener_country, market_symbol, symbol, candle):
    headers = {"User-Agent": "Mozilla/5.0"}
    url = f"https://scanner.tradingview.com/{screener_country}/scan"

    payload = {
        "symbols": {
            "tickers": ["{}:{}".format(market_symbol, symbol)],
            "query": {"types": []},
        },
        "columns": [
            "Recommend.Other|{}".format(candle),
            "Recommend.All|{}".format(candle),
            "Recommend.MA|{}".format(candle),
            "RSI|{}".format(candle),
            "RSI[1]|{}".format(candle),
            "Stoch.K|{}".format(candle),
            "Stoch.D|{}".format(candle),
            "Stoch.K[1]|{}".format(candle),
            "Stoch.D[1]|{}".format(candle),
            "CCI20|{}".format(candle),
            "CCI20[1]|{}".format(candle),
            "ADX|{}".format(candle),
            "ADX+DI|{}".format(candle),
            "ADX-DI|{}".format(candle),
            "ADX+DI[1]|{}".format(candle),
            "ADX-DI[1]|{}".format(candle),
            "AO|{}".format(candle),
            "AO[1]|{}".format(candle),
            "Mom|{}".format(candle),
            "Mom[1]|{}".format(candle),
            "MACD.macd|{}".format(candle),
            "MACD.signal|{}".format(candle),
            "Rec.Stoch.RSI|{}".format(candle),
            "Stoch.RSI.K|{}".format(candle),
            "Rec.WR|{}".format(candle),
            "W.R|{}".format(candle),
            "Rec.BBPower|{}".format(candle),
            "BBPower|{}".format(candle),
            "Rec.UO|{}".format(candle),
            "UO|{}".format(candle),
            "EMA10|{}".format(candle),
            "close|{}".format(candle),
            "SMA10|{}".format(candle),
            "EMA20|{}".format(candle),
            "SMA20|{}".format(candle),
            "EMA30|{}".format(candle),
            "SMA30|{}".format(candle),
            "EMA50|{}".format(candle),
            "SMA50|{}".format(candle),
            "EMA100|{}".format(candle),
            "SMA100|{}".format(candle),
            "EMA200|{}".format(candle),
            "SMA200|{}".format(candle),
            "Rec.Ichimoku|{}".format(candle),
            "Ichimoku.BLine|{}".format(candle),
            "Rec.VWMA|{}".format(candle),
            "VWMA|{}".format(candle),
            "Rec.HullMA9|{}".format(candle),
            "HullMA9|{}".format(candle),
            "Pivot.M.Classic.S3|{}".format(candle),
            "Pivot.M.Classic.S2|{}".format(candle),
            "Pivot.M.Classic.S1|{}".format(candle),
            "Pivot.M.Classic.Middle|{}".format(candle),
            "Pivot.M.Classic.R1|{}".format(candle),
            "Pivot.M.Classic.R2|{}".format(candle),
            "Pivot.M.Classic.R3|{}".format(candle),
            "Pivot.M.Fibonacci.S3|{}".format(candle),
            "Pivot.M.Fibonacci.S2|{}".format(candle),
            "Pivot.M.Fibonacci.S1|{}".format(candle),
            "Pivot.M.Fibonacci.Middle|{}".format(candle),
            "Pivot.M.Fibonacci.R1|{}".format(candle),
            "Pivot.M.Fibonacci.R2|{}".format(candle),
            "Pivot.M.Fibonacci.R3|{}".format(candle),
            "Pivot.M.Camarilla.S3|{}".format(candle),
            "Pivot.M.Camarilla.S2|{}".format(candle),
            "Pivot.M.Camarilla.S1|{}".format(candle),
            "Pivot.M.Camarilla.Middle|{}".format(candle),
            "Pivot.M.Camarilla.R1|{}".format(candle),
            "Pivot.M.Camarilla.R2|{}".format(candle),
            "Pivot.M.Camarilla.R3|{}".format(candle),
            "Pivot.M.Woodie.S3|{}".format(candle),
            "Pivot.M.Woodie.S2|{}".format(candle),
            "Pivot.M.Woodie.S1|{}".format(candle),
            "Pivot.M.Woodie.Middle|{}".format(candle),
            "Pivot.M.Woodie.R1|{}".format(candle),
            "Pivot.M.Woodie.R2|{}".format(candle),
            "Pivot.M.Woodie.R3|{}".format(candle),
            "Pivot.M.Demark.S1|{}".format(candle),
            "Pivot.M.Demark.Middle|{}".format(candle),
            "Pivot.M.Demark.R1|{}".format(candle),
        ],
    }

    try:
        resp = await requests.post(
            url, headers=headers, data=json.dumps(payload), timeout=60, verify=False
        )
    except requests.exceptions.ConnectionError:
        print("Connection error, retrying in 60 seconds")
        await asyncio.sleep(60)
        return

    resp = resp.json()
    # pprint(resp["data"][0]["d"])
    try:
        recommend_all = oscillator = float(resp["data"][0]["d"][1])
        recommend_other = float(resp["data"][0]["d"][0])
        recommend_ma = float(resp["data"][0]["d"][2])
    except (TypeError, IndexError) as exception:
        if exception == TypeError:
            pprint("TypeError")
            signal, recommend_other, recommend_ma = 0.0
        else:
            pprint("IndexError")
            return
    # timestamp
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #pprint(f"{timestamp} : {market_symbol} : {symbol} : {candle} : {recommend_all}")
    if recommend_all > 0.6 or recommend_all < -0.6:
        res = await get_ticker(symbol)
        vol = await calc_volume(res)
        price = res["lastPrice"]
        #if vol < 5000000:  # 24h volume less than 1M
        #    return
        dict_ = {}
        dict_["market"] = market_symbol
        dict_["symbol"] = symbol
        dict_["candle_interval"] = int(candle)
        dict_["price"] = float(price)
        dict_["recommend_all"] = float(recommend_all)
        dict_["recommend_ma"] = float(recommend_ma)
        dict_["recommend_other"] = float(recommend_other)
        await symbol_vol_calc(dict_)
        async with aiofiles.open(f"{market_symbol}-{symbol}.txt", mode="a") as f:
            await f.write(
                f"{timestamp} : {market_symbol} : {symbol} : {candle} : {recommend_all} : {price}\n"
            )
        #pprint(
        #    f"{timestamp} : {market_symbol} : {symbol} : {candle} : {recommend_all} : {price} : {vol}\n"
        #)


async def symbol_vol_calc(data):
    data = Trview_recommend(
        price=data["price"],
        market=data["market"],
        symbol=data["symbol"],
        candle_interval=data["candle_interval"],
        recommend_all=data["recommend_all"],
        recommend_ma=data["recommend_ma"],
        recommend_other=data["recommend_other"],
    )
    # Create an in-memory SQLite database engine
    engine = create_engine(DevelopmentConfig.DATABASE, echo=False)
    # Create a session factory
    Session = sessionmaker(bind=engine)
    session = Session()
    # Add the data to the session
    session.add(data)
    # Commit the changes to the database
    session.commit()

def get_by_volume(limit=300):
    engine = create_engine(DevelopmentConfig.DATABASE, echo=False)
    # Create a session factory
    Session = sessionmaker(bind=engine)
    session = Session()
    # First 300 item
    res = session.query(Symbol24_h_volume).order_by(Symbol24_h_volume.volume.desc()).limit(limit)
    for item in res:
        yield item.to_dict() 

async def process_item(semaphore, item):
    while True:
        async with semaphore:
            pprint(item["symbol"])
            await get_signal("crypto", "BINANCE", item["symbol"], "30")

async def main():
    tasks = []
    semaphore = asyncio.Semaphore(5)  # limit to <x> concurrent tasks
    # filter only binance symbols
    tasks = [
        process_item(semaphore, item)
        for item in get_by_volume(limit=100)
        #if item["market"] == "BINANCE"
        #and (item["symbol"].endswith("USDT") or item["symbol"].endswith("BUSD"))
    ]
    test = [
        item["symbol"]
        for item in get_by_volume(limit=100)
        #if item["market"] == "BINANCE"
        #and (item["symbol"].endswith("USDT") or item["symbol"].endswith("BUSD"))
    ]
    # create tasks
    # pprint(tasks) # list of coroutines
    pprint(test)
    pprint(len(tasks))

    await asyncio.gather(*tasks)  # this wr

if __name__ == "__main__":
    asyncio.run(main())
    # for item in get_symbols("crypto"):
    #    if item['market'] == "BINANCE":
    #        signal = get_signal("crypto", item['market'], item['symbol'], "15")
    #        pprint(signal)
