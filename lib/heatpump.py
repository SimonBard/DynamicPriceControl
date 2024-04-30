import json
import lib.mymqtt
import numpy
import lib.ha_connection
from dotenv import load_dotenv


class Heatpump:

  def __init__(self):   
    self._heating_curve = '{"zone1":{"heat":{"target":{"high":35,"low":25},"outside":{"high":20,"low":-15}},"cool":{"target":{"high":35,"low":25},"outside":{"high":15,"low":-15}}},"zone2":{"heat":{"target":{"high":35,"low":25},"outside":{"high":15,"low":-15}},"cool":{"target":{"high":35,"low":25},"outside":{"high":15,"low":-15}}}}'
    #self._increased_heating_curve = ""
    self._simple_namespace = json.loads(self._heating_curve)
    myha_connection = lib.ha_connection.ha_link()

    if myha_connection.set_zone1_heat_target_low() is not None:
      self._simple_namespace['zone1']['heat']['target']['low'] = int(float(myha_connection.set_zone1_heat_target_low()))
    if myha_connection.set_zone1_heat_target_high() is not None:
      self._simple_namespace['zone1']['heat']['target']['high'] = int(float(myha_connection.set_zone1_heat_target_high()))
    self.validate()
    
  def validate(self):
    MINIMUM = 25 # heatpump minimum target temperature is 25°C
    if self._simple_namespace['zone1']['heat']['target']['high'] < MINIMUM:
      self._simple_namespace['zone1']['heat']['target']['high'] = MINIMUM
    if self._simple_namespace['zone1']['heat']['target']['low'] < MINIMUM:
      self._simple_namespace['zone1']['heat']['target']['low'] = MINIMUM
 
  def adapt_heating_curve(self, delta):
    #print ('target high from ha connection is: ' , self._simple_namespace['zone1']['heat']['target']['high'])
    self._simple_namespace['zone1']['heat']['target']['high']+=delta 
    self._simple_namespace['zone1']['heat']['target']['low']+=delta 
    self.validate()
    json_data = json.dumps(self._simple_namespace)
    return json_data

  def send_original_heating_curve(self):
    inst = lib.mymqtt.Mqtt()
    inst.mqtt_publish_heatpump(self.adapt_heating_curve(0))

  def send_adapted_heating_curve(self, delta):
    inst = lib.mymqtt.Mqtt()
    inst.mqtt_publish_heatpump( self.adapt_heating_curve(delta))

  def calculate_tTargetCurrent(self, t_outside):
    tTargetHigh = self._simple_namespace['zone1']['heat']['target']['high']
    tTargetLow = self._simple_namespace['zone1']['heat']['target']['low']
    tOutsideHigh = self._simple_namespace['zone1']['heat']['outside']['high']
    tOutsideLow = self._simple_namespace['zone1']['heat']['outside']['low']

    tTargetCurrent =  tTargetLow + (tTargetHigh-tTargetLow)/(tOutsideHigh-tOutsideLow)*(tOutsideHigh-t_outside)
    return tTargetCurrent
  
  def calculateCOP(self, t_outside):
    # fromT is the outside Temperature
    # to T is the temperature that 
    tTargetHigh = self._simple_namespace['zone1']['heat']['target']['high']
    tTargetLow = self._simple_namespace['zone1']['heat']['target']['low']
    tOutsideHigh = self._simple_namespace['zone1']['heat']['outside']['high']
    tOutsideLow = self._simple_namespace['zone1']['heat']['outside']['low']

    tTargetCurrent =  tTargetLow + (tTargetHigh-tTargetLow)/(tOutsideHigh-tOutsideLow)*(tOutsideHigh-t_outside)
    print('tTargetCurrent ', tTargetCurrent)

    cop_matrix = numpy.array([       \
      [ 0,  25,	35,	45,	55,	60], \
      [-20,	2.39,	1.98,	1.61,	1.35,	1], \
      [-15,	2.75,	2.33,	1.87,	1.51,	1], \
      [-7,	3.27,	2.81,	2.23,	1.86,	1.72], \
      [2,	4.11,	3.4,	2.74,	2.16,	2], \
      [7,	6.15,	4.76,	3.57,	2.82,	2.53], \
      [25,	10.63,	7.7,	4.92,	3.72,	3.49], \
      ])

    # find next values 
     
    column_number = int(cop_matrix.size/cop_matrix[0].size)
    row_number = cop_matrix[0].size

    for y in range(1, row_number+1):
      cop_matrix[y,0]+=50
    t_outside+=50
    #print(cop_matrix)

    for x in range(0, column_number):
      #print(cop_matrix[x,0])
      if t_outside < cop_matrix[x,0]:
        x_high_index = x
        x_low_index = x-1
        break
    for y in range(0, row_number):
      if tTargetCurrent < cop_matrix[0,y]:
        y_high_index = y
        y_low_index = y-1
        break
    reg_tout_lower = cop_matrix[x_low_index, y_high_index] + (cop_matrix[x_low_index,y_low_index]-cop_matrix[x_low_index, y_high_index])/(cop_matrix[0, y_high_index]-cop_matrix[0, y_low_index])*(cop_matrix[0, y_high_index]-tTargetCurrent)
    reg_tout_higher = cop_matrix[x_high_index, y_high_index] + (cop_matrix[x_high_index,y_low_index]-cop_matrix[x_high_index, y_high_index])/(cop_matrix[0, y_high_index]-cop_matrix[0, y_low_index])*(cop_matrix[0, y_high_index]-tTargetCurrent)
    reg_tout_total = reg_tout_higher + (reg_tout_lower-reg_tout_higher)/(cop_matrix[x_high_index, 0] -cop_matrix[x_low_index, 0])*(cop_matrix[x_high_index, 0]-t_outside)

    # The calculation is correct, but based on the experience the matrix is too high. 
    # We should reduce the calculated COP to be trueful 
    reg_tout_total = 0.8* reg_tout_total
    return reg_tout_total

def main():
  MyHeatpump = Heatpump()
  print(MyHeatpump.calculateCOP(9))
  print(MyHeatpump.calculate_tTargetCurrent(9))
  print(MyHeatpump._simple_namespace['zone1']['heat']['target']['high'])
  print(MyHeatpump._simple_namespace['zone1']['heat']['target']['low'])
  #MyHeatpump.send_original_heating_curve()

  

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