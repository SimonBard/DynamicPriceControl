from solcast import live
from solcast import forecast
import os
from dotenv import load_dotenv

#import solcast
import urllib.request, json 
import datetime
import pandas as pd


class Solcast:

  def __init__(self):
    solcast_api_key = os.getenv('SOLCAST_API_KEY')
    rooftop = os.getenv('ROOFTOP')
    self._url = f"https://api.solcast.com.au/rooftop_sites/{rooftop}/forecasts?format=json&PT60M&api_key={solcast_api_key}"
    

  def retrieveSolcastData(self):  
    with urllib.request.urlopen(self._url) as url:
       data_json = json.load(url)
    #data = '{"forecasts": [{"pv_estimate": 0.2292, "pv_estimate10": 0.1017, "pv_estimate90": 0.4079, "period_end": "2024-04-09T09:30:00.0000000Z", "period": "PT30M"}, {"pv_estimate": 0.4134, "pv_estimate10": 0.1571, "pv_estimate90": 0.7219, "period_end": "2024-04-09T10:00:00.0000000Z", "period": "PT30M"}, {"pv_estimate": 0.9229, "pv_estimate10": 0.3967, "pv_estimate90": 1.4287, "period_end": "2024-04-09T10:30:00.0000000Z", "period": "PT30M"}, {"pv_estimate": 1.3919, "pv_estimate10": 0.8363, "pv_estimate90": 1.8839, "period_end": "2024-04-09T11:00:00.0000000Z", "period": "PT30M"}, {"pv_estimate": 1.4863, "pv_estimate10": 1.0199, "pv_estimate90": 2.0911, "period_end": "2024-04-09T11:30:00.0000000Z", "period": "PT30M"}, {"pv_estimate": 1.5441, "pv_estimate10": 0.82, "pv_estimate90": 2.9464, "period_end": "2024-04-09T12:00:00.0000000Z", "period": "PT30M"}, {"pv_estimate": 1.729, "pv_estimate10": 1.0896, "pv_estimate90": 2.5479, "period_end": "2024-04-09T12:30:00.0000000Z", "period": "PT30M"}, {"pv_estimate": 1.7629, "pv_estimate10": 1.238, "pv_estimate90": 2.5699, "period_end": "2024-04-09T13:00:00.0000000Z", "period": "PT30M"}, {"pv_estimate": 1.7938, "pv_estimate10": 1.238, "pv_estimate90": 2.585, "period_end": "2024-04-09T13:30:00.0000000Z", "period": "PT30M"}, {"pv_estimate": 1.7673, "pv_estimate10": 1.1692, "pv_estimate90": 2.5656, "period_end": "2024-04-09T14:00:00.0000000Z", "period": "PT30M"}, {"pv_estimate": 1.6926, "pv_estimate10": 1.0682, "pv_estimate90": 2.5047, "period_end": "2024-04-09T14:30:00.0000000Z", "period": "PT30M"}, {"pv_estimate": 1.5542, "pv_estimate10": 0.9504, "pv_estimate90": 2.3807, "period_end": "2024-04-09T15:00:00.0000000Z", "period": "PT30M"}, {"pv_estimate": 1.4315, "pv_estimate10": 0.8372, "pv_estimate90": 2.2824, "period_end": "2024-04-09T15:30:00.0000000Z", "period": "PT30M"}, {"pv_estimate": 1.3619, "pv_estimate10": 0.7288, "pv_estimate90": 2.2773, "period_end": "2024-04-09T16:00:00.0000000Z", "period": "PT30M"}, {"pv_estimate": 1.2057, "pv_estimate10": 0.5649, "pv_estimate90": 2.1451, "period_end": "2024-04-09T16:30:00.0000000Z", "period": "PT30M"}, {"pv_estimate": 0.9126, "pv_estimate10": 0.3829, "pv_estimate90": 1.7228, "period_end": "2024-04-09T17:00:00.0000000Z", "period": "PT30M"}, {"pv_estimate": 0.5952, "pv_estimate10": 0.2011, "pv_estimate90": 1.1911, "period_end": "2024-04-09T17:30:00.0000000Z", "period": "PT30M"}, {"pv_estimate": 0.1608, "pv_estimate10": 0.0748, "pv_estimate90": 0.5843, "period_end": "2024-04-09T18:00:00.0000000Z", "period": "PT30M"}, {"pv_estimate": 0.0031, "pv_estimate10": 0.0031, "pv_estimate90": 0.0031, "period_end": "2024-04-09T18:30:00.0000000Z", "period": "PT30M"}, {"pv_estimate": 0, "pv_estimate10": 0, "pv_estimate90": 0, "period_end": "2024-04-09T19:00:00.0000000Z", "period": "PT30M"}, {"pv_estimate": 0, "pv_estimate10": 0, "pv_estimate90": 0, "period_end": "2024-04-09T19:30:00.0000000Z", "period": "PT30M"}, {"pv_estimate": 0, "pv_estimate10": 0, "pv_estimate90": 0, "period_end": "2024-04-09T20:00:00.0000000Z", "period": "PT30M"}, {"pv_estimate": 0, "pv_estimate10": 0, "pv_estimate90": 0, "period_end": "2024-04-09T20:30:00.0000000Z", "period": "PT30M"}, {"pv_estimate": 0, "pv_estimate10": 0, "pv_estimate90": 0, "period_end": "2024-04-09T21:00:00.0000000Z", "period": "PT30M"}, {"pv_estimate": 0, "pv_estimate10": 0, "pv_estimate90": 0, "period_end": "2024-04-09T21:30:00.0000000Z", "period": "PT30M"}, {"pv_estimate": 0, "pv_estimate10": 0, "pv_estimate90": 0, "period_end": "2024-04-09T22:00:00.0000000Z", "period": "PT30M"}, {"pv_estimate": 0, "pv_estimate10": 0, "pv_estimate90": 0, "period_end": "2024-04-09T22:30:00.0000000Z", "period": "PT30M"}, {"pv_estimate": 0, "pv_estimate10": 0, "pv_estimate90": 0, "period_end": "2024-04-09T23:00:00.0000000Z", "period": "PT30M"}, {"pv_estimate": 0, "pv_estimate10": 0, "pv_estimate90": 0, "period_end": "2024-04-09T23:30:00.0000000Z", "period": "PT30M"}, {"pv_estimate": 0, "pv_estimate10": 0, "pv_estimate90": 0, "period_end": "2024-04-10T00:00:00.0000000Z", "period": "PT30M"}, {"pv_estimate": 0, "pv_estimate10": 0, "pv_estimate90": 0, "period_end": "2024-04-10T00:30:00.0000000Z", "period": "PT30M"}, {"pv_estimate": 0, "pv_estimate10": 0, "pv_estimate90": 0, "period_end": "2024-04-10T01:00:00.0000000Z", "period": "PT30M"}, {"pv_estimate": 0, "pv_estimate10": 0, "pv_estimate90": 0, "period_end": "2024-04-10T01:30:00.0000000Z", "period": "PT30M"}, {"pv_estimate": 0, "pv_estimate10": 0, "pv_estimate90": 0, "period_end": "2024-04-10T02:00:00.0000000Z", "period": "PT30M"}, {"pv_estimate": 0, "pv_estimate10": 0, "pv_estimate90": 0, "period_end": "2024-04-10T02:30:00.0000000Z", "period": "PT30M"}, {"pv_estimate": 0, "pv_estimate10": 0, "pv_estimate90": 0, "period_end": "2024-04-10T03:00:00.0000000Z", "period": "PT30M"}, {"pv_estimate": 0, "pv_estimate10": 0, "pv_estimate90": 0, "period_end": "2024-04-10T03:30:00.0000000Z", "period": "PT30M"}, {"pv_estimate": 0, "pv_estimate10": 0, "pv_estimate90": 0, "period_end": "2024-04-10T04:00:00.0000000Z", "period": "PT30M"}, {"pv_estimate": 0, "pv_estimate10": 0, "pv_estimate90": 0, "period_end": "2024-04-10T04:30:00.0000000Z", "period": "PT30M"}, {"pv_estimate": 0, "pv_estimate10": 0, "pv_estimate90": 0, "period_end": "2024-04-10T05:00:00.0000000Z", "period": "PT30M"}, {"pv_estimate": 0.0599, "pv_estimate10": 0.0383, "pv_estimate90": 0.062895, "period_end": "2024-04-10T05:30:00.0000000Z", "period": "PT30M"}, {"pv_estimate": 0.1368, "pv_estimate10": 0.1212, "pv_estimate90": 0.14364000000000002, "period_end": "2024-04-10T06:00:00.0000000Z", "period": "PT30M"}, {"pv_estimate": 0.2098, "pv_estimate10": 0.2053, "pv_estimate90": 0.22028999999999999, "period_end": "2024-04-10T06:30:00.0000000Z", "period": "PT30M"}, {"pv_estimate": 0.3244, "pv_estimate10": 0.3182, "pv_estimate90": 0.34062000000000003, "period_end": "2024-04-10T07:00:00.0000000Z", "period": "PT30M"}, {"pv_estimate": 0.5625, "pv_estimate10": 0.4807, "pv_estimate90": 0.5906250000000001, "period_end": "2024-04-10T07:30:00.0000000Z", "period": "PT30M"}, {"pv_estimate": 0.989, "pv_estimate10": 0.675, "pv_estimate90": 1.03845, "period_end": "2024-04-10T08:00:00.0000000Z", "period": "PT30M"}, {"pv_estimate": 1.4263, "pv_estimate10": 0.8626, "pv_estimate90": 1.4793, "period_end": "2024-04-10T08:30:00.0000000Z", "period": "PT30M"}, {"pv_estimate": 1.906, "pv_estimate10": 1.0414, "pv_estimate90": 2.0617, "period_end": "2024-04-10T09:00:00.0000000Z", "period": "PT30M"}, {"pv_estimate": 2.3847, "pv_estimate10": 1.1639, "pv_estimate90": 2.624, "period_end": "2024-04-10T09:30:00.0000000Z", "period": "PT30M"}, {"pv_estimate": 2.7832, "pv_estimate10": 1.2162, "pv_estimate90": 3.1306, "period_end": "2024-04-10T10:00:00.0000000Z", "period": "PT30M"}, {"pv_estimate": 3.0664, "pv_estimate10": 1.2057, "pv_estimate90": 3.5813, "period_end": "2024-04-10T10:30:00.0000000Z", "period": "PT30M"}, {"pv_estimate": 3.163, "pv_estimate10": 1.105, "pv_estimate90": 3.9257, "period_end": "2024-04-10T11:00:00.0000000Z", "period": "PT30M"}, {"pv_estimate": 3.2777, "pv_estimate10": 1.0575, "pv_estimate90": 4.2265, "period_end": "2024-04-10T11:30:00.0000000Z", "period": "PT30M"}, {"pv_estimate": 3.4041, "pv_estimate10": 1.0522, "pv_estimate90": 4.431, "period_end": "2024-04-10T12:00:00.0000000Z", "period": "PT30M"}, {"pv_estimate": 3.4832, "pv_estimate10": 1.0364, "pv_estimate90": 4.5942, "period_end": "2024-04-10T12:30:00.0000000Z", "period": "PT30M"}, {"pv_estimate": 3.4624, "pv_estimate10": 0.9994, "pv_estimate90": 4.654, "period_end": "2024-04-10T13:00:00.0000000Z", "period": "PT30M"}, {"pv_estimate": 3.3632, "pv_estimate10": 0.9305, "pv_estimate90": 4.6726, "period_end": "2024-04-10T13:30:00.0000000Z", "period": "PT30M"}, {"pv_estimate": 3.1202, "pv_estimate10": 0.8303, "pv_estimate90": 4.5662, "period_end": "2024-04-10T14:00:00.0000000Z", "period": "PT30M"}, {"pv_estimate": 2.791, "pv_estimate10": 0.6969, "pv_estimate90": 4.4359, "period_end": "2024-04-10T14:30:00.0000000Z", "period": "PT30M"}, {"pv_estimate": 2.3497, "pv_estimate10": 0.544, "pv_estimate90": 4.2269, "period_end": "2024-04-10T15:00:00.0000000Z", "period": "PT30M"}, {"pv_estimate": 2.069, "pv_estimate10": 0.4624, "pv_estimate90": 3.8947, "period_end": "2024-04-10T15:30:00.0000000Z", "period": "PT30M"}, {"pv_estimate": 1.9962, "pv_estimate10": 0.4297, "pv_estimate90": 3.5152, "period_end": "2024-04-10T16:00:00.0000000Z", "period": "PT30M"}, {"pv_estimate": 1.7363, "pv_estimate10": 0.3256, "pv_estimate90": 2.9753, "period_end": "2024-04-10T16:30:00.0000000Z", "period": "PT30M"}, {"pv_estimate": 1.3546, "pv_estimate10": 0.2063, "pv_estimate90": 2.4268, "period_end": "2024-04-10T17:00:00.0000000Z", "period": "PT30M"}, {"pv_estimate": 0.8899, "pv_estimate10": 0.1295, "pv_estimate90": 1.768, "period_end": "2024-04-10T17:30:00.0000000Z", "period": "PT30M"}, {"pv_estimate": 0.374, "pv_estimate10": 0.0548, "pv_estimate90": 1.038, "period_end": "2024-04-10T18:00:00.0000000Z", "period": "PT30M"}, {"pv_estimate": 0.0062, "pv_estimate10": 0.0031, "pv_estimate90": 0.0288, "period_end": "2024-04-10T18:30:00.0000000Z", "period": "PT30M"}, {"pv_estimate": 0, "pv_estimate10": 0, "pv_estimate90": 0, "period_end": "2024-04-10T19:00:00.0000000Z", "period": "PT30M"}, {"pv_estimate": 0, "pv_estimate10": 0, "pv_estimate90": 0, "period_end": "2024-04-10T19:30:00.0000000Z", "period": "PT30M"}, {"pv_estimate": 0, "pv_estimate10": 0, "pv_estimate90": 0, "period_end": "2024-04-10T20:00:00.0000000Z", "period": "PT30M"}, {"pv_estimate": 0, "pv_estimate10": 0, "pv_estimate90": 0, "period_end": "2024-04-10T20:30:00.0000000Z", "period": "PT30M"}, {"pv_estimate": 0, "pv_estimate10": 0, "pv_estimate90": 0, "period_end": "2024-04-10T21:00:00.0000000Z", "period": "PT30M"}, {"pv_estimate": 0, "pv_estimate10": 0, "pv_estimate90": 0, "period_end": "2024-04-10T21:30:00.0000000Z", "period": "PT30M"}, {"pv_estimate": 0, "pv_estimate10": 0, "pv_estimate90": 0, "period_end": "2024-04-10T22:00:00.0000000Z", "period": "PT30M"}, {"pv_estimate": 0, "pv_estimate10": 0, "pv_estimate90": 0, "period_end": "2024-04-10T22:30:00.0000000Z", "period": "PT30M"}, {"pv_estimate": 0, "pv_estimate10": 0, "pv_estimate90": 0, "period_end": "2024-04-10T23:00:00.0000000Z", "period": "PT30M"}, {"pv_estimate": 0, "pv_estimate10": 0, "pv_estimate90": 0, "period_end": "2024-04-10T23:30:00.0000000Z", "period": "PT30M"}, {"pv_estimate": 0, "pv_estimate10": 0, "pv_estimate90": 0, "period_end": "2024-04-11T00:00:00.0000000Z", "period": "PT30M"}, {"pv_estimate": 0, "pv_estimate10": 0, "pv_estimate90": 0, "period_end": "2024-04-11T00:30:00.0000000Z", "period": "PT30M"}, {"pv_estimate": 0, "pv_estimate10": 0, "pv_estimate90": 0, "period_end": "2024-04-11T01:00:00.0000000Z", "period": "PT30M"}, {"pv_estimate": 0, "pv_estimate10": 0, "pv_estimate90": 0, "period_end": "2024-04-11T01:30:00.0000000Z", "period": "PT30M"}, {"pv_estimate": 0, "pv_estimate10": 0, "pv_estimate90": 0, "period_end": "2024-04-11T02:00:00.0000000Z", "period": "PT30M"}, {"pv_estimate": 0, "pv_estimate10": 0, "pv_estimate90": 0, "period_end": "2024-04-11T02:30:00.0000000Z", "period": "PT30M"}, {"pv_estimate": 0, "pv_estimate10": 0, "pv_estimate90": 0, "period_end": "2024-04-11T03:00:00.0000000Z", "period": "PT30M"}, {"pv_estimate": 0, "pv_estimate10": 0, "pv_estimate90": 0, "period_end": "2024-04-11T03:30:00.0000000Z", "period": "PT30M"}, {"pv_estimate": 0, "pv_estimate10": 0, "pv_estimate90": 0, "period_end": "2024-04-11T04:00:00.0000000Z", "period": "PT30M"}, {"pv_estimate": 0, "pv_estimate10": 0, "pv_estimate90": 0, "period_end": "2024-04-11T04:30:00.0000000Z", "period": "PT30M"}, {"pv_estimate": 0, "pv_estimate10": 0, "pv_estimate90": 0, "period_end": "2024-04-11T05:00:00.0000000Z", "period": "PT30M"}, {"pv_estimate": 0.0706, "pv_estimate10": 0.0359, "pv_estimate90": 0.07413, "period_end": "2024-04-11T05:30:00.0000000Z", "period": "PT30M"}, {"pv_estimate": 0.1593, "pv_estimate10": 0.0904, "pv_estimate90": 0.167265, "period_end": "2024-04-11T06:00:00.0000000Z", "period": "PT30M"}, {"pv_estimate": 0.2873, "pv_estimate10": 0.134, "pv_estimate90": 0.301665, "period_end": "2024-04-11T06:30:00.0000000Z", "period": "PT30M"}, {"pv_estimate": 0.3977, "pv_estimate10": 0.1975, "pv_estimate90": 0.41758500000000004, "period_end": "2024-04-11T07:00:00.0000000Z", "period": "PT30M"}, {"pv_estimate": 0.6489, "pv_estimate10": 0.3187, "pv_estimate90": 0.6813450000000001, "period_end": "2024-04-11T07:30:00.0000000Z", "period": "PT30M"}, {"pv_estimate": 1.0077, "pv_estimate10": 0.4382, "pv_estimate90": 1.0580850000000002, "period_end": "2024-04-11T08:00:00.0000000Z", "period": "PT30M"}, {"pv_estimate": 1.4272, "pv_estimate10": 0.5396, "pv_estimate90": 1.4932, "period_end": "2024-04-11T08:30:00.0000000Z", "period": "PT30M"}, {"pv_estimate": 1.8227, "pv_estimate10": 0.6234, "pv_estimate90": 2.0347, "period_end": "2024-04-11T09:00:00.0000000Z", "period": "PT30M"}, {"pv_estimate": 2.2162, "pv_estimate10": 0.6776, "pv_estimate90": 2.571, "period_end": "2024-04-11T09:30:00.0000000Z", "period": "PT30M"}]}'
    #data_json = json.loads(data)
    return data_json
  
  def process_json(self):
    json = self.retrieveSolcastData()
    df = pd.DataFrame.from_dict(json['forecasts'], orient='columns')
    df['period_end'] = pd.to_datetime(df['period_end'], format='ISO8601')
    df_aggregated =  df.resample('60min', on='period_end').sum()
    
    list = []
    for index, row in df_aggregated.iterrows():
        #print(row.name, row.name.date(), row.name.hour, row.pv_estimate)
        dict = {"timestamp": row.name, "date": row.name.date(), "hour": row.name.hour, "pv_estimate": row.pv_estimate}
        list.append(dict)

    return list

def old():
    SOLCAST_API_KEY  = os.getenv(SOLCAST_API_KEY)
    
    res = forecast.rooftop_pv_power(
        latitude = os.getenv('LATITUDE'),
        longitude = os.getenv('LONGITUDE'),
        tilt = os.getenv('DECLINATION'),
        azimuth = os.getenv('AZIMUTH'),
        capacity = os.getenv('KWP'),
        period='PT60M',
        api_key = SOLCAST_API_KEY,
        #output_parameters='pv_power_rooftop'
    )
    df = res.to_pandas()


    print('solcast')

def main():
   inst = Solcast()
   inst.process_json()

if __name__ == "__main__":
    main()


