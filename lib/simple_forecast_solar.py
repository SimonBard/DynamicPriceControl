import asyncio

from forecast_solar import ForecastSolar
import lib.manager
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

from urllib import request
from bs4 import BeautifulSoup
import json



class Forecast:

    def __init__(self):
        pass
        
    def forecast_tomorrow(self):
        # Make a request
        latitude = os.getenv('LATITUDE')
        longitude = os.getenv('LONGITUDE')
        declination = os.getenv('DECLINATION')
        azimuth = os.getenv('AZIMUTH')
        kwp = os.getenv('KWP')


        try:
            url = f"https://api.forecast.solar/estimate/watthours/day/{latitude}/{longitude}/{declination}/{azimuth}/{kwp}/"
            html = request.urlopen(url).read()
            soup = BeautifulSoup(html,'html.parser')
            site_json=json.loads(soup.text)
            result_dict = site_json['result']
            #print(result_dict)
            values = result_dict.values()
            for item in values:
                #print(item)
                forecast_tomorrow = item/1000
            print('Vorhersage für morgen ist: ', forecast_tomorrow)
            return forecast_tomorrow
        except Exception as e:
            print(e)
            pass
        
        #print(type(site_json))
       

    

def main():
    print('this is forecast-solar!')
    inst = Forecast()   
    SManager = lib.manager.Manager()
    tomorrow = (datetime.now() + timedelta(1)).strftime('%Y-%m-%d')
    SManager.write_pv_forecast(tomorrow, inst.forecast_tomorrow())


if __name__ == "__main__":
    main()