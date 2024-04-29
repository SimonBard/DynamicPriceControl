import asyncio

from forecast_solar import ForecastSolar
import lib.manager
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv


class Forecast:

    def __init__(self):
        
        #self._market_area = market_area
        
        self._estimate = []

    async def start(self):
        # await self.tibber_connection.update_info()
        # print(self.tibber_connection.name)
        home = await self.fetch()
        # await self.tibber_connection.close_connection()
        return home

    async def fetch(self):
        """Show example on how to use the library."""
        async with ForecastSolar(
            api_key="",
            latitude=49.50589,
            longitude=7.03035,
            declination=35,
            azimuth=160,
            kwp=5.67,
            damping=0,
            damping_morning=0,
            damping_evening=0,
            #horizon="0,0,0,10,10,20,20,30,30",
        ) as forecast:
            estimate = await forecast.estimate()
            
            return estimate


async def main():
    


if __name__ == "__main__":
    asyncio.run(main())