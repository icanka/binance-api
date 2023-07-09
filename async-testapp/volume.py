import asyncio
from trview.models import Symbol24HVolume, commit_session
from trview.config import DevelopmentConfig
from binance import AsyncClient
from binance.exceptions import BinanceAPIException
from pprint import pprint
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


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
    #pprint(res)
    return res


async def calc_volume(response):
    pprint(response)
    return float(response['volume'])*float(response['lastPrice'])


async def main(symbol="PROSUSDT"):
    res = await get_ticker(symbol)
    vol = await calc_volume(res)
    vol = Symbol24HVolume(symbol=symbol, volume=vol)
    database = 'sqlite://///home/izzetcan/Documents/git-repos/binance-api/flask_app/instance/trading.development.sqlite'
    # Create an in-memory SQLite database engine
    pprint(DevelopmentConfig.DATABASE)
    engine = create_engine(database, echo=True)
    # Create a session factory
    Session = sessionmaker(bind=engine)
    session = Session()
    # Add the data to the session
    session.add(vol)
    # Commit the changes to the database
    session.commit()

    
    
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    finally:  # cleanup in case of error
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()
