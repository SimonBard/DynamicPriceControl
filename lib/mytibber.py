import tibber.const
import tibber
import asyncio
import os
from dotenv import load_dotenv
import aiohttp

class Tibber:

  def __init__(self):
    
    self._url = 'blabla'
    self._temperaturedata = []

  load_dotenv()
  ACCESS_TOKEN = os.getenv('TIBBER_ACCESS_TOKEN')

  tibber_connection = tibber.Tibber(ACCESS_TOKEN, user_agent="change_this")

  async def _home_data(self):
    home = self.tibber_connection.get_homes()[0]
    await home.fetch_consumption_data()
    await home.update_info()
    #print(home.address1)

    await home.update_price_info()
    #print(home._price_info)

    return home

  async def start(self):
  
    async with aiohttp.ClientSession() as session:
        tibber_connection = tibber.Tibber(self.ACCESS_TOKEN, websession=session, user_agent="change_this")
        await tibber_connection.update_info()
    home = tibber_connection.get_homes()[0]
    return home
  


def main():
  loop = asyncio.get_event_loop()
  inst = Tibber()
  home = loop.run_until_complete(inst.start())  
  
  print(home)
 
  for key in home._price_info:
      print(key , home._price_info[key])
  ''' 
  The home object is a class tibber.home.TibberHome and has properties:
      _price_info is a dictionary object
      address1 is the adress of the home

  '''

if __name__ == "__main__":
    main()