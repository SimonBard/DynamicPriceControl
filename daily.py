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
#import lib.my_forecast_solar

def main():
    print('Run daily routine')
    mymanager = lib.manager.Manager()
    data_temperature = mymanager.get_temperatures()
    mymanager.write_temperature_data(data_temperature)

    inst = lib.mytibber.Tibber()
    loop = asyncio.get_event_loop()
    home = loop.run_until_complete(inst.start())  
    mymanager.write_tibber_data(home)

    inst = lib.pv_solcast.Solcast()
    forecast = inst.process_json()
    for element in forecast:
        mymanager.write_element_to_hourly_values(element['date'], element['hour'], 'pv_forecast', element['pv_estimate'])

    today = (datetime.now() + timedelta(0)).strftime('%Y-%m-%d')
    tomorrow = (datetime.now() + timedelta(1)).strftime('%Y-%m-%d')
    

    if datetime.now().hour > 13:
        hourly_values = mymanager.retrieve_dict(tomorrow)
    else:
        hourly_values = mymanager.retrieve_dict(today)
    n=0
    for element in hourly_values:
        #print(n, hourly_values[n][5], hourly_values[n][3])
        heatprice_perkwh = element['tibber_brutto'] / element['cop_specific'] # so lange noch kein Forecast vorhanden, wird hier tibber_brutto übernommen
        mymanager.write_heatprice(element['date'], element['hour'], heatprice_perkwh)
        n=n+1
    if datetime.now().hour > 13:
        hourly_values = mymanager.retrieve_dict(tomorrow)
    else:
        hourly_values = mymanager.retrieve_dict(today)
    x_cheapest_hours_hp = sorted(hourly_values, key=lambda d:d['heatprice_perkwh'])[:6]
    x_expensive_hours_hp = sorted(hourly_values, reverse=True, key=lambda d:d['heatprice_perkwh'])[:6]
    x_cheapest_hours = sorted(hourly_values, key=lambda d:d['tibber_brutto'])[:2]
    x_expensive_hours = sorted(hourly_values, reverse=True, key=lambda d:d['tibber_brutto'])[:5]

    if x_expensive_hours[0]['heatprice_perkwh'] > x_cheapest_hours[0]['heatprice_perkwh']*1.15:
        print('price difference is large enough')
        mymanager.write_load_battery(x_cheapest_hours[0]['date'], x_cheapest_hours[0]['hour'], True)
    else: 
        print('price difference not large enough to load battery')

    for element in x_expensive_hours:
        mymanager.write_load_battery(element['date'], element['hour'], False)

    for element in x_expensive_hours_hp:
        mymanager.write_statehp_recommendation(element['date'], element['hour'], False)

    for element in x_cheapest_hours_hp:
        mymanager.write_statehp_recommendation(element['date'], element['hour'], True)

    inst = lib.manager.Manager()
    demand = inst.demand_retrieve_dict()
    for n in range(0, len(demand)-1):
        try:
            homeconsumption = demand[n]['total_home_consumption'] - demand[n-1]['total_home_consumption']
            #print (demand[n]['date'], demand[n]['total_home_consumption'], homeconsumption)
            print('write consumption for date' , demand[n]['date'], demand[n]['total_home_consumption'], homeconsumption)
            inst.write_demand(demand[n]['date'], 'home_consumption', homeconsumption)
            print('write production for date' , demand[n]['date'])
            pv_production = demand[n]['pv_totalyield'] - demand[n-1]['pv_totalyield']
            inst.write_demand(demand[n]['date'], 'pv_production', pv_production)
        except Exception as e:
            print(e)

    print('this is forecast-solar!')
    inst = lib.simple_forecast_solar.Forecast()   
    SManager = lib.manager.Manager()
    tomorrow = (datetime.now() + timedelta(1)).strftime('%Y-%m-%d')
    SManager.write_pv_forecast(tomorrow, inst.forecast_tomorrow())

    

if __name__ == "__main__":
    main()


