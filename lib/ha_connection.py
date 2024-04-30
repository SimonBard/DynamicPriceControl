from requests import get
import json
import os
from dotenv import load_dotenv


class ha_link:
    def __init__(self):
        load_dotenv()
        authorization = "Bearer " + os.getenv('HA_AUTHORIZATION')
        self.url_start = os.getenv('HA_URL')
        self.headers =  {
        "Authorization": authorization,
        "content-type": "application/json",
        }
       
    def charge_switch(self):
        item = "input_boolean.speicher_sofort_laden"
        if self.state_request_switch(item) is not None:
            return(self.state_request_switch(item))
        else:
            return 'off'
        
    def minsoc_attempt(self):
        item = "input_number.speicher_minsoc_attempt"
        if self.state_request_integer(item) is not None:
            return(self.state_request_integer(item))
        else:
            return 'off'
    
    def simon_battery_control(self):
        item = "input_boolean.simon_battery_control"
        if self.state_request_switch(item) is not None:
            return(self.state_request_switch(item))
        else:
            return 'on'
    
    def simon_wp_control(self):
        item = "input_boolean.simon_wp_control"
        if self.state_request_switch(item) is not None:
            return(self.state_request_switch(item))
        else:
            return 'on'
    
    def set_zone1_heat_target_high(self):
        item= "input_number.set_zone1_heat_target_high"
        return(self.state_request_integer(item))
    
    def set_zone1_heat_target_low(self):
        item= "input_number.set_zone1_heat_target_low"
        return(self.state_request_integer(item))

    def state_request_switch(self, item):
        url = self.url_start + item
        response = get(url, headers=self.headers)
        try:
            d = json.loads(response.text)
            #print(d)
            state = d['state']
        except Exception as e:
            print('Message from HA was: ',e)
            print('did not get valid response from homeassistant for: ', item)
            state = None   
        return state
    
    def state_request_integer(self, item):
        url = self.url_start + item
        response = get(url, headers=self.headers)
        try:
            d = json.loads(response.text)
            #print (d)
            state = d['state']
        except Exception as e:
            print('Message from HA was: ',e)
            print('did not get valid response from homeassistant, set to standard value')
            state = None
        return state
        

def main():
    inst = ha_link()
    status = inst.charge_switch()['state']
    minsoc = inst.minsoc_attempt()['state']
    print(status)
    print(minsoc)


if __name__ == "__main__":
    main()