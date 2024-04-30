# DynamicElectricityPriceControl

The script is very basic right now, but will be more advanced in the future. 
Its a beta phase, the code is not very beautiful and not following basic coding conventions, but will be corrected. 

## Sponsoring
If you would like to support me, you can use my code to register for tibber: 5f218fz1
https://invite.tibber.com/5f218fz1

You will get 50€ for their store and at least right now in Germany, you get also 30€ discount for an ADAC membership (I can provide a ADAC number if you do not have one). 
You can also just make a new contract with tibber to get the voucher of 50€. 

## How it works
To make it simple: 
- The battery can be charged if the price difference during the day exceeds 5 ct/kWh
- You can manually charge the battery if you like

- The heatpump will use a higher target temperature (or more speficially heating curve) when the electricity price is low and use a lower target temperature if the price is high. 

- If there is enough PV power (> 2000W) and the battery is charged > 80%, the target temperature is set even a bit higher. 
Why is this useful?
Usually the heatpump uses a heat curve, so it adapts the water temperature to the outside temperature. The problem is: Especially in spring when you have some PV power, the heatpump will run much as the outside temperature is high. So you will use only a small fraction of the self-generated power. At night, temperatures decreases but you have not excess PV power. 

## What you need
- heishamon as an addon to the Panasonic heatpump to control the heatpump via MQTT
- PV inverter from KOSTAL
- an MQTT broker (with heishamon connected to it)
- docker installed (for statistics and to store some values)

optional: 
- telegram to get status messages
- homeassistant installed

## Setup and Configuration

Download the files to a directory of your choice.

1. Start a docker container with postgre SQL.
   You need to adapt the volume to your needs. Please choose a safe password instead of secret123$%.
   
```
docker run -d --name postgres-heatpump -e POSTGRES_PASSWORD=secret123$% -e PGDATA=/var/lib/postgresql/data/pgdata -v /intenso/docker/volumes/postgre:/var/lib/postgresql/data --network nextcloudpi -p 8071:8080 -v /etc/timezone:/etc/timezone:ro -v /etc/localtime:/etc/localtime:ro -p 5432:5432 postgres
```


Also adapt the database.ini file with that password.

2.  Install requirements
Its recommended to use a virtual environment, but I want to make it as easy as possible here. 
```
python3 -m pip install -r requirements.txt
```
3. Init the database with
```
python3 setup.py
```

4. Adapt the .env file. Put in your data in the .env.example file and delete the ending .example. The file name should be .env

5. Add the following helpers in homeassistant if available: 
simon_battery_control (as switch)
Speicher_sofort_laden (as switch)
speicher_minsoc_attempt (as number)
simon_wp_control (as switch)
Set_zone1.heat.target.low (as number)
Set_zone1.heat.target.high (as number)

If you do not use homeassistant, the script will use some default values. 

6. Test the script
```
python3 daily.py 
python3 minutely.py
```

This should not invoke any error

7. set cron jobs: 
```
00 16 * * * python3 /intenso/docker/volumes/postgre/python/daily.py
*/1 * * * *  python3 /intenso/docker/volumes/postgre/python/minutely.py 
```
I just mention the full path here to have a better example, adapt the path to your filesystem.

## Feedback
If you had difficulties with the docu, readme or you have any suggestions, open a discussion here on github. 

I am open to develop more integrations for other inverter, heatpumps etc. To do so, I will need access to your local network for a limited time to make the tests. If you are open to it, just open an issue to get in contact with me. Please provide info about your setup. 

