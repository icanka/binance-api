import asyncio
import aiofiles
from binance import AsyncClient, BinanceSocketManager

async def write_to_file(file, data):
    await file.write(data)

async def order_book(client, symbol):
    order_book = await client.get_order_book(symbol=symbol)
    print(order_book)

async def kline_listener(client):
    bm = BinanceSocketManager(client)
    symbol = "BTCUSDT"
    res_count = 0
    
    async with aiofiles.open("kline.txt", mode="w") as f:
        async with bm.kline_socket(symbol=symbol) as stream:
            while True:
                res = await stream.recv()
                res_count += 1
                print(res)
                loop.call_soon(asyncio.create_task, write_to_file(f, str(res)))
                if res_count == 1000:
                    res_count = 0
                    print("1000 klines received")
                    break
                    #loop.call_soon(asyncio.create_task, order_book(client, symbol))
            
async def main_0():
    client = await AsyncClient.create()
    await kline_listener(client)

async def main_1():
    client = await AsyncClient.create()
    res = await asyncio.gather(client.get_exchange_info(), client.get_all_tickers())


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main_0())
    finally: # cleanup in case of error
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()
        
