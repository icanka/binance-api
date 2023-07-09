import asyncio
import aiofiles
import aiohttp
from binance import AsyncClient, BinanceSocketManager
from pprint import pprint


async def write_to_file(file, data):
    await file.write(data)


async def get_order_book(client, symbol):
    order_book = await client.get_order_book(symbol=symbol)
    print(order_book)


async def kline_listener(client):
    bm = BinanceSocketManager(client)
    symbol = "BTCUSDT"
    res_count = 0
    async with aiofiles.open("kline.txt", mode="w") as f:
        async with bm.kline_socket(symbol=symbol, interval=AsyncClient.KLINE_INTERVAL_30MINUTE) as stream:
            while True:
                res = await stream.recv()
                res_count += 1
                print(res)
                loop.call_soon(asyncio.create_task, write_to_file(f, str(res)))
                if res_count == 1000:
                    res_count = 0
                    print("1000 klines received")
                    break
                    # loop.call_soon(asyncio.create_task, order_book(client, symbol))


async def mini_ticker_socket(client):
    bm = BinanceSocketManager(client)
    res_count = 0
    async with aiofiles.open("mini_ticker.txt", mode="w") as f:
        while True:
            async with bm.miniticker_socket() as stream:
                res = await stream.recv()
                res_count += 1
                print(res)
                loop.call_soon(asyncio.create_task, write_to_file(f, str(res)))


async def get_ticker_price(client, symbol):
    async with aiofiles.open(f"{symbol}-TICKER.txt", mode="w") as f:
        while True:
            await asyncio.sleep(0.5)
            res = await client.get_ticker(symbol=symbol)
            res2 = await client.get_symbol_ticker(symbol=symbol)
            pprint(res2)
            #print(type(res))
            print(res['lastPrice'])
            #pprint(res['volume'])
            # conver price and volume to float
            price = float(res['lastPrice'])
            volume = float(res['volume'])
            pprint(price*volume)
            #await client.close_connection()
            await write_to_file(f, str(res))

async def main_0():
    client = await AsyncClient.create()
    await kline_listener(client)


async def main_socket_ticker():
    client = await AsyncClient.create()
    await mini_ticker_socket(client)


async def main_ticker(symbol):
    client = await AsyncClient.create()
    await get_ticker_price(client, symbol)


async def main_1():
    client = await AsyncClient.create()
    res = await asyncio.gather(client.get_exchange_info(), client.get_all_tickers())
    print(res)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main_ticker("PROSUSDT"))
    finally:  # cleanup in case of error
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()
