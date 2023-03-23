from __future__ import print_function # use python 3 syntax but make it compatible with python 2
from __future__ import division       #                           ''

import time     # import the time library for the sleep function
import brickpi3 # import the BrickPi3 drivers
import numpy as np

BP = brickpi3.BrickPi3()

base_speed = 200

WHEEL_RADIUS = 2.8
AXIS_RADIUS = 6.6

BP.set_sensor_type(BP.PORT_1, BP.SENSOR_TYPE.TOUCH)
BP.set_sensor_type(BP.PORT_4, BP.SENSOR_TYPE.TOUCH)

def reset_encoder():
    BP.offset_motor_encoder(BP.PORT_A, BP.get_motor_encoder(BP.PORT_A))
    BP.offset_motor_encoder(BP.PORT_D, BP.get_motor_encoder(BP.PORT_D))

def setup_BP():
    reset_encoder()
    BP.set_motor_position_kp(BP.PORT_A,25)
    BP.set_motor_position_kd(BP.PORT_A,70)
    BP.set_motor_limits(BP.PORT_A,100,250)

    BP.set_motor_position_kp(BP.PORT_D,25)
    BP.set_motor_position_kd(BP.PORT_D,70)
    BP.set_motor_limits(BP.PORT_D,100,250)

    BP.set_sensor_type(BP.PORT_1, BP.SENSOR_TYPE.TOUCH)
    BP.set_sensor_type(BP.PORT_2, BP.SENSOR_TYPE.TOUCH)


def stop_and_back():
    # stop
    BP.set_motor_power(BP.PORT_A, 0)
    BP.set_motor_power(BP.PORT_D, 0)
    time.sleep(1)
    BP.set_motor_position(BP.PORT_A, -720)
    BP.set_motor_position(BP.PORT_D, -720)
    time.sleep(2)
    reset_encoder()

def rotate_left(alpha):
    #alpha = angle in radians
    encoder_value = int(alpha*AXIS_RADIUS* 180/(np.pi * WHEEL_RADIUS))
    BP.set_motor_position(BP.PORT_A, encoder_value)
    BP.set_motor_position(BP.PORT_D, -encoder_value)
    BP.offset_motor_encoder(BP.PORT_A, BP.get_motor_encoder(BP.PORT_A))
    BP.offset_motor_encoder(BP.PORT_D, BP.get_motor_encoder(BP.PORT_D))
    time.sleep(2)

def rotate_right(alpha):
    #alpha = angle in radians
    encoder_value = int(alpha*AXIS_RADIUS* 180/(np.pi * WHEEL_RADIUS))
    BP.set_motor_position(BP.PORT_A, -encoder_value)
    BP.set_motor_position(BP.PORT_D, encoder_value)
    BP.offset_motor_encoder(BP.PORT_A, BP.get_motor_encoder(BP.PORT_A))
    BP.offset_motor_encoder(BP.PORT_D, BP.get_motor_encoder(BP.PORT_D))
    time.sleep(2)

def move_forward(dps):
    """Direction: 0=straight, {1,-1}=rotate
    dsp>0:move forward, dps<0: move backwards"""
    BP.set_motor_dps(BP.PORT_A, dps)
    BP.set_motor_dps(BP.PORT_D, dps)
    time.sleep(0.02)
    reset_encoder()

def check_sensor():
    
    try:
        value1 = BP.get_sensor(BP.PORT_1)
        value2 = BP.get_sensor(BP.PORT_4)
        value = [value1, value2]
        print(value)

    except brickpi3.SensorError as error:
        value = error
        print(error)
        
    return value

def adapt(flags):
    sensors_activated = [i for i, x in enumerate(flags) if x]
    if len(sensors_activated)>0: # if sensor toggled
        stop_and_back()
        if len(sensors_activated)==2: # sensors_activated = [0,1]
            move_forward(base_speed)
        else:
            if sensors_activated[0]==0:
                rotate_right(np.pi/2 * 1.02)
            else:
                rotate_left(np.pi/2 * 1.02)
            move_forward(base_speed)

def run():
    setup_BP()
    move_forward(base_speed)
    while True:
        flags = []
        flags = check_sensor()
        if any(flags):
            adapt(flags)
        time.sleep(0.5)

if __name__== "__main__":
    try:
        try:
           run()
        except IOError as error:
            print(error)
        time.sleep(0.02)
    except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
        BP.reset_all()        # Unconfigure the sensors, disable the motors, and restore the LED to the control of the BrickPi3 firmware.

