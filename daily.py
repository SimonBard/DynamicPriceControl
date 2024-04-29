# the daily routine should retrieve all the data from the database and decide at 
# which hour to load the battery and switch on the heat pump. 
# I recommend to run it at 23:00 (best temperature data and energy prices are available)

#!/usr/bin/python

#import python.dbmanager as dbmanager
import lib.manager
import lib.mytibber
import lib.pv_solcast
import lib.simple_forecast_solar
from forecast_solar import ForecastSolar
from datetime import datetime, timedelta
import asyncio
import lib.weather
#import lib.my_forecast_solar

def process_temperature_forecast():
    dbmanager = lib.manager.Manager()
    myweather = lib.weather.Weather()
    data_temperature = myweather.fetch()
    dbmanager.write_temperature_data(data_temperature)

def process_tibber():
    inst = lib.mytibber.Tibber()
    loop = asyncio.get_event_loop()
    home = loop.run_until_complete(inst.start())  
    mymanager = lib.manager.Manager()
    mymanager.write_tibber_data(home)

def process_pv_solast():
    mymanager = lib.manager.Manager()
    inst = lib.pv_solcast.Solcast()
    forecast = inst.process_json()
    for element in forecast:
        mymanager.write_element_to_hourly_values(element['date'], element['hour'], 'pv_forecast', element['pv_estimate'])

def process_recommendations():
    today = (datetime.now() + timedelta(0)).strftime('%Y-%m-%d')
    tomorrow = (datetime.now() + timedelta(1)).strftime('%Y-%m-%d')
    
    dbmanager = lib.manager.Manager()
    if datetime.now().hour > 13:
        hourly_values = dbmanager.retrieve_dict(tomorrow)
    else:
        hourly_values = dbmanager.retrieve_dict(today)
    n=0
    for element in hourly_values:
        #print(n, hourly_values[n][5], hourly_values[n][3])
        heatprice_perkwh = element['tibber_brutto'] / element['cop_specific'] # so lange noch kein Forecast vorhanden, wird hier tibber_brutto übernommen
        dbmanager.write_heatprice(element['date'], element['hour'], heatprice_perkwh)
        n=n+1
    
    if datetime.now().hour > 13:
        hourly_values = dbmanager.retrieve_dict(tomorrow)
    else:
        hourly_values = dbmanager.retrieve_dict(today)
    x_cheapest_hours_hp = sorted(hourly_values, key=lambda d:d['heatprice_perkwh'])[:6]
    x_expensive_hours_hp = sorted(hourly_values, reverse=True, key=lambda d:d['heatprice_perkwh'])[:8]
    x_cheapest_hours = sorted(hourly_values, key=lambda d:d['tibber_brutto'])[:2]
    x_expensive_hours = sorted(hourly_values, reverse=True, key=lambda d:d['tibber_brutto'])[:5]

    if x_expensive_hours[0]['heatprice_perkwh'] > x_cheapest_hours[0]['heatprice_perkwh']*1.15:
        print('price difference is large enough')
        dbmanager.write_load_battery(x_cheapest_hours[0]['date'], x_cheapest_hours[0]['hour'], True)
    else: 
        print('price difference not large enough to load battery')

    for element in x_expensive_hours:
        dbmanager.write_load_battery(element['date'], element['hour'], False)

    for element in x_expensive_hours_hp:
        dbmanager.write_statehp_recommendation(element['date'], element['hour'], False)

    for element in x_cheapest_hours_hp:
        dbmanager.write_statehp_recommendation(element['date'], element['hour'], True)

def process_stats():
    dbmanager = lib.manager.Manager()
    demand = dbmanager.demand_retrieve_dict()
    for n in range(0, len(demand)-1):
        try:
            homeconsumption = demand[n]['total_home_consumption'] - demand[n-1]['total_home_consumption']
            dbmanager.write_demand(demand[n]['date'], 'home_consumption', homeconsumption)
            pv_production = demand[n]['pv_totalyield'] - demand[n-1]['pv_totalyield']
            dbmanager.write_demand(demand[n]['date'], 'pv_production', pv_production)
        except Exception as e:
            print(e)

    timerange = -10
    for td in range (timerange,0):
        day = (datetime.now() + timedelta(td)).strftime('%Y-%m-%d')
        hourly_values = dbmanager.retrieve_dict(day)
        solcast_daily_sum = 0
        temperature_daily_sum = 0
        for n in range(0, len(hourly_values)):
            try:
                solcast_daily_sum=  solcast_daily_sum + hourly_values[n]['pv_forecast']
                temperature_daily_sum=  temperature_daily_sum + hourly_values[n]['t_forecast']
            except Exception as e:
                print(e)
        dbmanager.write_demand(str(day), 'solcast', solcast_daily_sum)
        temperature_average = temperature_daily_sum/24
        dbmanager.write_demand(str(day), 'temperature_avg', temperature_average)

def process_forecast_solar():
    print('this is forecast-solar!')
    inst = lib.simple_forecast_solar.Forecast()   
    SManager = lib.manager.Manager()
    tomorrow = (datetime.now() + timedelta(1)).strftime('%Y-%m-%d')
    SManager.write_pv_forecast(tomorrow, inst.forecast_tomorrow())

def main():
    print('Run daily routine')
    process_temperature_forecast()
    process_tibber()
    process_pv_solast()
    process_recommendations()
    process_forecast_solar()
    process_stats()

if __name__ == "__main__":
    main()


