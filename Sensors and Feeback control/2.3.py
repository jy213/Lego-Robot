#!/usr/bin/env python
#
# https://www.dexterindustries.com/BrickPi/
# https://github.com/DexterInd/BrickPi3
#
# Copyright (c) 2016 Dexter Industries
# Released under the MIT license (http://choosealicense.com/licenses/mit/).
# For more information, see https://github.com/DexterInd/BrickPi3/blob/master/LICENSE.md
#
# This code is an example for reading an NXT ultrasonic sensor connected to PORT_1 of the BrickPi3
# 
# Hardware: Connect an NXT ultrasonic sensor to BrickPi3 Port 1.
# 
# Results:  When you run this program, you should see the distance in CM.

from __future__ import print_function # use python 3 syntax but make it compatible with python 2
from __future__ import division       #                           ''

import time     # import the time library for the sleep function
import brickpi3 # import the BrickPi3 drivers

BP = brickpi3.BrickPi3() # Create an instance of the BrickPi3 class. BP will be the BrickPi3 object.
BP.set_sensor_type(BP.PORT_2, BP.SENSOR_TYPE.NXT_ULTRASONIC)

value = 0
# Configure for an NXT ultrasonic sensor.
# BP.set_sensor_type configures the BrickPi3 for a specific sensor.
# BP.PORT_1 specifies that the sensor will be on sensor port 1.
# BP.SENSOR_TYPE.NXT_ULTRASONIC specifies that the sensor will be an NXT ultrasonic sensor.

def get_median(data):
    data.sort()
    half = len(data) // 2
    return (data[half] + data[~half]) / 2

def get_sonar_value():
    while True:
        try:
            value = BP.get_sensor(BP.PORT_2)
            print(value) 
            return value# print the distance in CM
        except brickpi3.SensorError as error:
            print(error)
            

DESIRED_DISTANCE = 30
Kp = 10
CONSTANT_SPEED = 100

index = 0
sonar_list=[100,100,100,100]

BP.set_motor_dps(BP.PORT_A, CONSTANT_SPEED)
BP.set_motor_dps(BP.PORT_D, CONSTANT_SPEED)

while True:
    if(index<3):
        sonar_list[index] = get_sonar_value()
        print("inputing, ",sonar_list[index])
        index += 1
    else:
        print(sonar_list)
        print("foward")
        median = get_median(sonar_list)
        DIFFERENCE = (median - DESIRED_DISTANCE) * Kp
        print("velocity, ", DIFFERENCE)
        
        
        
        BP.set_motor_dps(BP.PORT_A, CONSTANT_SPEED - 0.5*DIFFERENCE)
        BP.set_motor_dps(BP.PORT_D, CONSTANT_SPEED + 0.5*DIFFERENCE)
        time.sleep(0.5)
        index = 0










