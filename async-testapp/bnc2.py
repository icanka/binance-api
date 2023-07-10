import asyncio
from trview.models import Symbol24_h_volume, commit_session
from trview.config import DevelopmentConfig
from binance import AsyncClient
from binance.exceptions import BinanceAPIException
from pprint import pprint
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from binance.client import Client


# def get_symbols(screener_country):
#     headers = {"User-Agent": "Mozilla/5.0"}
#     url = "https://scanner.tradingview.com/{}/scan".format(screener_country)
#     symbol_lists = requests_sync.post(
#         url, headers=headers, timeout=10).json()
#     data = symbol_lists["data"]
#     for pair in data:
#         data = pair["s"].split(":")
#         _dict = {"symbol": data[1], "market": data[0]}
#         yield _dict

def get_symbols():
    client = Client()
    res = client.get_all_tickers()
    for item in res:
        yield item['symbol']


async def calc_volume(response):
    return float(response['volume'])*float(response['lastPrice'])


async def get_ticker(symbol):
    client = await AsyncClient.create()
    try:
        res = await client.get_ticker(symbol=symbol)
    except BinanceAPIException:
        pprint(f"Error getting ticker for {symbol}")
        await client.close_connection()
        pprint(f"Connection closed for {symbol}")
        raise
    finally:
        await client.close_connection()
    # pprint(res)
    return res


async def symbol_vol_calc(symbol):
    res = await get_ticker(symbol)
    vol = await calc_volume(res)
    if vol == 0:
        return
    vol = Symbol24_h_volume(symbol=symbol, volume=vol)
    # Create an in-memory SQLite database engine
    engine = create_engine(DevelopmentConfig.DATABASE, echo=False)
    # Create a session factory
    Session = sessionmaker(bind=engine)
    session = Session()
    # Add the data to the session
    row = session.query(Symbol24_h_volume).filter_by(symbol=symbol).first()
    if row is not None:
        row.volume = vol.volume
    else:
        session.add(vol)
        # Commit the changes to the database
    session.commit()
    pprint(f"Volume for {symbol} is {vol.volume}")
    await asyncio.sleep(1)


async def process_item(semaphore, symbol):
    #while True:
    async with semaphore:
        await symbol_vol_calc(symbol)


async def main():
    # while True:
    tasks = []
    semaphore = asyncio.Semaphore(5)  # limit to <x> concurrent tasks
    # filter only binance symbols
    tasks = [
        process_item(semaphore, symbol)
        for symbol in get_symbols()
        if symbol.endswith("USDT") or symbol.endswith("BUSD")
    ]
    # create tasks
    # pprint(tasks) # list of coroutines
    await asyncio.gather(*tasks)  # this wr
    #await asyncio.sleep(43200)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    finally:  # cleanup in case of error
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()
