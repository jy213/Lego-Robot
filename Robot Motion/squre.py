from __future__ import print_function # use python 3 syntax but make it compatible with python 2
from __future__ import division       #                           ''

import time     # import the time library for the sleep function
import brickpi3 # import the BrickPi3 drivers

BP = brickpi3.BrickPi3() # Create an insta
import numpy as np


WHEEL_RADIUS = 2.8
AXIS_RADIUS = 6.6



def move_forward(distance):
    encoder_value = int(distance * 180/(np.pi * WHEEL_RADIUS))
    print(encoder_value)
    status_A = BP.get_motor_status(BP.PORT_A)
    print('motor A: ',status_A)
    status_D = BP.get_motor_status(BP.PORT_D)
    print('motor D: ',status_D)
    BP.set_motor_position(BP.PORT_A, encoder_value)
    BP.set_motor_position(BP.PORT_D, encoder_value)
    BP.offset_motor_encoder(BP.PORT_A, BP.get_motor_encoder(BP.PORT_A))
    BP.offset_motor_encoder(BP.PORT_D, BP.get_motor_encoder(BP.PORT_D))
    time.sleep(4)

def rotate(alpha):
    #alpha = angle in radians
    encoder_value = int(alpha*AXIS_RADIUS* 180/(np.pi * WHEEL_RADIUS))
    BP.set_motor_position(BP.PORT_A, encoder_value)
    print(encoder_value)
    BP.set_motor_position(BP.PORT_D, -encoder_value)
    BP.offset_motor_encoder(BP.PORT_A, BP.get_motor_encoder(BP.PORT_A))
    BP.offset_motor_encoder(BP.PORT_D, BP.get_motor_encoder(BP.PORT_D))
    time.sleep(4)

def run():
    BP.set_motor_position_kp(BP.PORT_A,25)
    BP.set_motor_position_kd(BP.PORT_A,70)
    BP.set_motor_limits(BP.PORT_A,200,250)

    BP.set_motor_position_kp(BP.PORT_D,25)
    BP.set_motor_position_kd(BP.PORT_D,70)
    BP.set_motor_limits(BP.PORT_D,200,250)

    for i in range(4):
        print("Run #:", i)
        print("Encoder positions:")
        print(BP.get_motor_encoder(BP.PORT_A),BP.get_motor_encoder(BP.PORT_D))
        print('Move forward')
        #print(WHEEL_RADIUS)
        #self.move_forward(66)
        move_forward(40.85) #distance in cm
        print(BP.get_motor_encoder(BP.PORT_A),BP.get_motor_encoder(BP.PORT_D))
        #print('Rotate')
        rotate(np.pi/2 * 1.02)
        print(BP.get_motor_encoder(BP.PORT_A),BP.get_motor_encoder(BP.PORT_D))

if __name__== "__main__":
    try:
        try:
            run()
        except IOError as error:
            print(error)
        time.sleep(0.02)
    except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
        BP.reset_all()        # Unconfigure the sensors, disable the motors, and restore the LED to the control of the BrickPi3 firmware.