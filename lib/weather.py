import aiohttp
import asyncio
import urllib.request
import json
from datetime import datetime, date, time, timedelta, timezone
from time import mktime
from typing import Any, Protocol
from typing_extensions import Final, Literal, TypeAlias, final
import os
from dotenv import load_dotenv
import validators


class Weather:

    def __init__(self):
        load_dotenv()
        self.LONG = os.getenv('WEATHER_LONG')
        self.LAT = os.getenv('WEATHER_LAT') 
        self.URL = f"https://api.open-meteo.com/v1/forecast?latitude={self.LAT}&longitude={self.LONG}&hourly=temperature_2m"
        if not validators.url(self.URL):
            print("You did not provide valid data for the weather api")
        #self._market_area = market_area
        self._url = self.URL.format()
        self._temperaturedata = []
        #print(self._url)
        
    # fetch data from awattar website:
    def _fetch_data(self, url):
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read())
        return data
            
    def fetch(self):
        data = self._fetch_data(self._url)
        #print('raw data: ', data)
        self._tempearturedata = self._extract_temperaturedata(data['hourly'])
        #print(self._tempearturedata)
        return self._tempearturedata

    def _extract_temperaturedata(self, hourly_data):
        entries = []
        time = hourly_data['time']
        temperature = hourly_data['temperature_2m']
        n = 0
        while n <= 62:
            entry = Temperature(time[n], temperature[n])
            entries.append(entry)
            n=n+1
        return entries
    

class Temperature:
    

    def __init__(self, time, temperature):
        #print(time)
        self._start_time = time
        # time = 2023-11-01T07:00

        datetime_object = datetime.strptime(time, '%Y-%m-%dT%H:%M')
        #self._start_time = time
        self._temperature = temperature

        self._date = datetime.date(datetime_object)
        self._hour = datetime_object.hour

    def __repr__(self):
        return f"{self.__class__.__name__}(time: {self._start_time}, date: {self._date}, hour: {self._hour}, temperature: {self._temperature})"  

    @property
    def start_time(self):
        return self._start_time
    
    @property
    def date(self):
        return self._date
    
    @property
    def hour(self):
        return self._hour

    @property
    def temperature(self):
        return self._temperature

                
def main():
    
    inst = Weather()
    data = inst.fetch()
    print(data)


if __name__ == "__main__":
    main()



