
import json
import time, datetime
import paho.mqtt.client as paho
import os
from dotenv import load_dotenv



class Mqtt:

    def __init__(self):
        self.topic = ""
        self.message = ""
        self.broker = os.getenv('MQTT_BROKER')
        self.port = 1883

    def mqtt_publish(self, topic, message):

        try:
            # Publish MQTT Message
            client1 = paho.Client("WP_control")  # create client object
            client1.connect(self.broker, self.port)  # establish connection

            client1.publish(topic, message)  # publish
            print('connected to broker and published:', topic, message)

        except Exception as e:
            print(e)
            pass

    def mqtt_publish_heatpump(self, message):

        try:
            # Publish MQTT Message
            client1 = paho.Client("WP_control")  # create client object
            client1.connect(self.broker, self.port)  # establish connection
            topic = 'panasonic_heat_pump/commands/SetCurves'
            client1.publish(topic, message)  # publish
            print('connected to broker and published:', topic, message)

        except Exception as e:
            print(e)
            pass
    
    def mqtt_publish_battery(self, message):

        try:
            # Publish MQTT Message
            client1 = paho.Client("Battery")  # create client object
            client1.connect(self.broker, self.port)  # establish connection

            client1.publish('Battery charging power is now ', message)  # publish
            print('connected to broker and published:', 'Battery', message)

        except Exception as e:
            print(e)
            pass

def main():
    
    Mqtt.mqtt_publish("WP_control/topic_to_switch_WP_on", "ON")

if __name__ == "__main__":
    main()

'''
SET5 	SetZ1HeatRequestTemperature 	Set Z1 heat shift or direct heat temperature 	-5 to 5 or 20 to max
SET7 	SetZ2HeatRequestTemperature 	Set Z2 heat shift or direct heat temperature 	-5 to 5 or 20 to max

or better set the whole heating curve:
SET16 	SetCurves 	Set zones heat/cool curves 	JSON document (see below)
{"zone1":{"heat":{"target":{"high":35,"low":25},"outside":{"high":15,"low":-15}},"cool":{"target":{"high":35,"low":25},"outside":{"high":15,"low":-15}}},"zone2":{"heat":{"target":{"high":35,"low":25},"outside":{"high":15,"low":-15}},"cool":{"target":{"high":35,"low":25},"outside":{"high":15,"low":-15}}}}

It can be checked with:
TOP29 	main/Z1_Heat_Curve_Target_High_Temp 	Target temperature at lowest point on the heating curve (°C)
TOP30 	main/Z1_Heat_Curve_Target_Low_Temp 	Target temperature at highest point on the heating curve (°C)
TOP31 	main/Z1_Heat_Curve_Outside_High_Temp 	Lowest outside temperature on the heating curve (°C)
TOP32 	main/Z1_Heat_Curve_Outside_Low_Temp 	Highest outside temperature on the heating curve (°C)

I suggest to just enhance the heating curve by some degrees
'''