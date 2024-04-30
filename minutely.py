# This routine should run every minute 

import lib.manager
import lib.heatpump
from datetime import datetime
import lib.battery
from requests import get
import lib.ha_connection
import lib.telegram
from dotenv import load_dotenv
import os


def main():

    stats()
    battery_charge_switch()
    wp()


def battery():
    load_dotenv()
    myha_link = lib.ha_connection.ha_link()
    mybattery = lib.battery.kostal_modbusquery()
    mybattery.run()

    timestamp = f'{datetime.now():%Y-%m-%d %H:%M:%S%z}'

    # Write yield and consumption values to database
    today = datetime.now().strftime('%Y-%m-%d')
    dbmanager = lib.manager.Manager()

    simon_battery_control = myha_link.simon_battery_control()
    print("simon_battery_control: ", simon_battery_control)
    if simon_battery_control ==  "on":
        hourly_values = dbmanager.retrieve_dict_from_hourly_values(today)
        current_hour = int(datetime.now().strftime("%H"))
 
        print (timestamp,'Battery load: ', hourly_values[current_hour]['load_battery'])
        print(timestamp,'Grid Power is: ', mybattery.getGridPower())
        if not hourly_values[current_hour]['load_battery']: # this means electricity is expensive
            print(timestamp,'energy is expensive right now. Let battery control itself') # do nothing, battery can be discharged

        if hourly_values[current_hour]['load_battery']:   # this means electricity is cheap  
                print(timestamp,'Battery should load now')
                mybattery.load_battery_1min(-5000)
                
        if mybattery.getPVProduction() < mybattery.getTotalHomeConsumption():
            print('Consumption is higher than production')
            if hourly_values[current_hour]['load_battery'] is None: 
                print(timestamp,'energy is neither expensive nor cheap. Hold SOC')
                mybattery.load_battery_1min(0)
        else: 
            print('Production is higher than consumption. Let battery control itself')
    else: 
        print("status_charge_switch is off, do nothing")


def wp():
    myha_link = lib.ha_connection.ha_link()
    mybattery = lib.battery.kostal_modbusquery()
    mybattery.run()

    timestamp = f'{datetime.now():%Y-%m-%d %H:%M:%S%z}'

    # Write yield and consumption values to database
    today = datetime.now().strftime('%Y-%m-%d')
    dbmanager = lib.manager.Manager()
    print('TotalAC2Grid is: ', mybattery.getTotalAC2Grid())
    mytelegram = lib.telegram.Telegram()
    simon_wp_control = myha_link.simon_wp_control()

    if simon_wp_control ==  "on":
        hourly_values = dbmanager.retrieve_dict_from_hourly_values(today)
        current_hour = int(datetime.now().strftime("%H"))
        
        myheatpump = lib.heatpump.Heatpump()
        print (timestamp,'state hp recommendation: ', hourly_values[current_hour]['statehp_recommendation'])
        print(timestamp,'Home Consumption is: ', mybattery.getTotalHomeConsumption())
        print(timestamp,'PV Production is: ', mybattery.getPVProduction())
        
        if int(dbmanager.getcounter()) > 0:
            myheatpump.send_adapted_heating_curve(delta=10)
        else:
            if  (mybattery.getPVProduction() > 2000 and mybattery.get_currentsoc() > 80) :   # this means electricity is cheap  
                print(timestamp,'PV is producing enough', mybattery.getPVProduction(), ' enhance heating curve')
                mytelegram.message_all(timestamp +' PV macht genug Strom' + str(mybattery.getPVProduction()) + ' erhöhe Heizkurve stärker')
                if int(dbmanager.getcounter()) < 1:
                    dbmanager.write_counter(30)
            else:
                if hourly_values[current_hour]['statehp_recommendation']:   # this means electricity is cheap  
                    print(timestamp,'Energy is cheap, enhance heating curve')
                    mytelegram.message_all(timestamp + ' Energie ist gerade billig, erhöhe Heizkurve leicht')
                    myheatpump.send_adapted_heating_curve(delta=5)    
                else:
                    #myheatpump.send_original_heating_curve()
                    if not hourly_values[current_hour]['statehp_recommendation']:  # this means electricity is expensive
                        print(timestamp,'energy is expensive right now, heatpump reduce temperature') # do nothing, battery can be discharged
                        mytelegram.message_all(timestamp + ' Energie ist gerade teuer, reduziere Heizkurve') # do nothing, battery can be discharged
                        myheatpump.send_adapted_heating_curve(delta=-10)
                    else:
                        print(timestamp,'energy is neither expensive nor cheap. Send original heating curve')
                        mytelegram.message_all(timestamp + ' Energie ist weder teuer noch billig. Sende originale Heizkurve')
                        myheatpump.send_original_heating_curve()
    else: 
        print("simon_wp_control is off, do nothing")
        mytelegram.message_all("simon_wp_control in homeassistant ist ausgeschaltet, WP macht was ihr zuletzt gesagt wurde oder manuell eingestellt wurde")


def battery_charge_switch():
    myha_link = lib.ha_connection.ha_link()
    mybattery = lib.battery.kostal_modbusquery()
    mybattery.run()

    status_charge_switch = myha_link.charge_switch()
    minsoc = myha_link.minsoc_attempt()
    current_soc = mybattery.get_currentsoc()
    timestamp = f'{datetime.now():%Y-%m-%d %H:%M:%S%z}'
    print('TotalAC2Grid is: ', mybattery.getTotalAC2Grid())

    mytelegram = lib.telegram.Telegram()

    if status_charge_switch == "on":
        if  float(minsoc) > float(current_soc):        
            print(timestamp, " status ist: ", status_charge_switch, "|| minsoc soll: ", minsoc, " soc ist: ", current_soc, "=> also lade")
            mytelegram.message_all(timestamp + " status ist: "+ str(status_charge_switch) +  "|| minsoc soll: "+ str(minsoc) + " soc ist: "+ str(current_soc) + "=> also lade")
            mybattery.load_battery_1min(-5000)
        else:
            print(timestamp, " status is: ", status_charge_switch, "|| minsoc soll: ", minsoc, " soc ist: ", current_soc)
            if mybattery.getGridPower() > 0:
                print(timestamp, "Netzbezug, deshalb nicht entladen oder laden")
                mybattery.load_battery_1min(0)
            else: 
                print(timestamp, "Netzeinspeisung, deshalb Steurung aufgeben, damit Akku von PV laden kann")
    else:
        print(timestamp, "Accu charge switch is off, do nothing")

def stats():
    mybattery = lib.battery.kostal_modbusquery()
    mybattery.run()

    # Write yield and consumption values to database
    today = datetime.now().strftime('%Y-%m-%d')
    dbmanager = lib.manager.Manager()
    dbmanager.write_demand(today, "pv_totalyield", mybattery.getTotalYield())
    dbmanager.write_demand(today, "total_home_consumption", mybattery.getTotalHomeConsumption())
    dbmanager.write_demand(today, 'totalac2grid', mybattery.getTotalAC2Grid())

if __name__ == "__main__":
    main()
 