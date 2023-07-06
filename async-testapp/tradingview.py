import asyncio
import datetime
import json
import aiofiles
import requests as requests_sync
import requests_async as requests
from pprint import pprint


def get_symbols(screener_country):
    headers = {"User-Agent": "Mozilla/5.0"}
    url = "https://scanner.tradingview.com/{}/scan".format(screener_country)
    symbol_lists = requests_sync.post(url, headers=headers, verify=False).json()
    data = symbol_lists["data"]
    for pair in data:
        data = pair["s"].split(":")
        dict = {"symbol": data[1], "market": data[0]}
        yield dict


async def get_signal(screener_country, market_symbol, symbol, candle):
    headers = {"User-Agent": "Mozilla/5.0"}
    url = "https://scanner.tradingview.com/{}/scan".format(screener_country)

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
    
    resp = await requests.post(
        url, headers=headers, data=json.dumps(payload), verify=False
    )
    resp = resp.json()
    try:
        signal = oscillator = resp["data"][0]["d"][1]
    # signal to fload
        signal = float(signal)
    except (TypeError, IndexError) as e:
        if e == TypeError:
            signal = 0.0
        else: return
    # timestamp
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if signal > 0.6:
        async with aiofiles.open(f"{market_symbol}-{symbol}.txt", mode="a") as f:
            await f.write(f"{timestamp} : {market_symbol} : {symbol} : {candle} : {signal}\n")
        pprint(f"{symbol} : {signal}")
    # return signal


async def process_item(semaphore, item):
    while True:
        async with semaphore:
            await get_signal("crypto", item["market"], item["symbol"], "30")


async def main():
    tasks = []
    semaphore = asyncio.Semaphore(100)  # limit to <x> concurrent tasks
    # filter only binance symbols
    tasks = [
        process_item(semaphore, item)
        for item in get_symbols("crypto")
        if item["market"] == "BINANCE"
    ]
    # create tasks
    #pprint(tasks) # list of coroutines

    await asyncio.gather(*tasks) # this wr


if __name__ == "__main__":
    asyncio.run(main())
    # for item in get_symbols("crypto"):
    #    if item['market'] == "BINANCE":
    #        signal = get_signal("crypto", item['market'], item['symbol'], "15")
    #        pprint(signal)
