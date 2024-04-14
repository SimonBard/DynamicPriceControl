import json
import time, datetime
import paho.mqtt.client as paho
import os
from dotenv import load_dotenv

broker = "192.168.103.44"
port = 1883

class Mqtt:

    def __init__(self):
        self.topic = ""
        self.message = ""

    def mqtt_publish(self, topic, message):

        try:
            # Publish MQTT Message
            client1 = paho.Client("python")  # create client object
            client1.connect(broker, port)  # establish connection

            client1.publish(topic, message)  # publish
            print('connected to broker and published:', topic, message)

        except Exception as e:
            print(e)
            pass

def main():
    # Using readlines()
    file1 = open('zigbee2mqtt2.log', 'r')
    Lines = file1.readlines()
    inst = Mqtt()
    
    count = 0
    # Strips the newline character
    for line in Lines:
        count += 1
        line = "Line{}: {}".format(count, line.strip())
        #print(line[69:108])
        topic_pos_start = line.find('topic')+7
        payload_pos = line.find('payload')
        topic_pos_end = payload_pos - 3
        topic = line[topic_pos_start:topic_pos_end]
        device = topic[21:][:18]
        tag = topic[:20]
        payload = line[payload_pos+9:][:-1]
        if tag == "homeassistant/sensor":
            #print (topic)
            #print('device',  device)
            #print (payload)
            if device == '0x00158d0004066f44':
                inst.mqtt_publish(topic, payload)






if __name__ == "__main__":
    main()
