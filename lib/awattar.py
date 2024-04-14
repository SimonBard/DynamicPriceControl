import aiohttp
import asyncio
import urllib.request
import json
from datetime import datetime, date, time, timedelta, timezone
from time import mktime
from typing import Any, Protocol
from typing_extensions import Final, Literal, TypeAlias, final
import math

def toEpochMilliSec(dt: datetime) -> int:
    return mktime(dt.timetuple()) * 1000


class Awattar:

    def __init__(self, market_area):
        
        self._market_area = market_area
        self._url = self.URL.format(market_area=market_area)
        self._marketdata = []

    URL = "https://api.awattar.de/v1/marketdata"
    MARKET_AREAS = ("at", "de")

    # fetch data from awattar website:
    def _fetch_data(self, url):
        #URL = "https://api.awattar.de/v1/marketdata"
        response = urllib.request.urlopen(url)
        data = json.loads(response.read())
        return data
            
    def fetch(self):
        data = self._fetch_data(self._url)
        self._marketdata = self._extract_marketdata(data["data"])
        return self._marketdata

    def _extract_marketdata(self, data):
        entries = []
        for entry in data:
            entries.append(Marketprice(entry))
        return entries
    

class Marketprice:
    UOM_EUR_PER_MWh = "EUR/MWh"

    def __init__(self, data):
        assert data["unit"].lower() == self.UOM_EUR_PER_MWh.lower()
        
        self._start_time = datetime.fromtimestamp(
            data["start_timestamp"] / 1000, tz=timezone.utc
        )
        self._end_time = datetime.fromtimestamp(
            data["end_timestamp"] / 1000, tz=timezone.utc
        )
        timestamp = datetime.fromtimestamp(
            data["start_timestamp"] / 1000, tz=timezone.utc)
        self._date = datetime.date(timestamp)
        self._hour = timestamp.hour

        self._price_eur_per_mwh = float(data["marketprice"])

    def __repr__(self):
        return f"{self.__class__.__name__}(hour: {self._hour}, date: {self._date}, start: {self._start_time.isoformat()}, end: {self._end_time.isoformat()}, marketprice: {self._price_eur_per_mwh} {self.UOM_EUR_PER_MWh})"  # noqa: E501

    @property
    def start_time(self):
        return self._start_time
    
    @property
    def start_time(self):
        return self._hour
    
    @property
    def date(self):
        return self._date

    @property
    def hour(self):
        return self._hour

    @property
    def end_time(self):
        return self._end_time

    @property
    def price_eur_per_mwh(self):
        return self._price_eur_per_mwh

    @property
    def price_ct_per_kwh(self):
        return self._price_eur_per_mwh / 10
    
    @property
    def brutto_price_ct_per_kwh(self):
        NETZGEB = 9.34
        UMSATZSTEUERFAKTOR = 1.19
        TIBBERGEB = 2.5
        STROMSTEUER = 2
        SONSTIGE = 4 # Konzessionsabgabe, KWK Umlage, ...
        brutto = (self.price_ct_per_kwh + NETZGEB + UMSATZSTEUERFAKTOR + TIBBERGEB + STROMSTEUER + SONSTIGE)*UMSATZSTEUERFAKTOR
        return brutto
                
def main():
    
    inst = Awattar("de")
    data = inst.fetch()
    print(data)

if __name__ == "__main__":
    main()



