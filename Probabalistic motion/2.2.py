from __future__ import print_function # use python 3 syntax but make it compatible with python 2
from __future__ import division      #    

import time     # import the time library for the sleep function
import brickpi3 # import the BrickPi3 drivers
import numpy as np
import random
import math
import matplotlib                      

BP = brickpi3.BrickPi3() # Create an insta


DISTANCE = 10
NUMBER_OF_PARTICLES = 100
WEIGHT = 1/NUMBER_OF_PARTICLES 
ANGLE = 90
FULL_PARTICLE_LIST = []

WHEEL_RADIUS = 2.8
AXIS_RADIUS = 6.6

CURRENT_X = 0
CURRENT_Y = 0
CURRENT_THETA = 0
K_F = 1.06
K_T = 1.18

def move_forward(distance):
    encoder_value = int(distance * 180/(np.pi * WHEEL_RADIUS))
    BP.set_motor_position(BP.PORT_A, encoder_value)
    BP.set_motor_position(BP.PORT_D, encoder_value)
    BP.offset_motor_encoder(BP.PORT_A, BP.get_motor_encoder(BP.PORT_A))
    BP.offset_motor_encoder(BP.PORT_D, BP.get_motor_encoder(BP.PORT_D))
    time.sleep(4)

def rotate_left(alpha):
    #alpha = angle in radians
    encoder_value = int(alpha*AXIS_RADIUS* 180/(np.pi * WHEEL_RADIUS))
    BP.set_motor_position(BP.PORT_A, encoder_value)
    BP.set_motor_position(BP.PORT_D, -encoder_value)
    BP.offset_motor_encoder(BP.PORT_A, BP.get_motor_encoder(BP.PORT_A))
    BP.offset_motor_encoder(BP.PORT_D, BP.get_motor_encoder(BP.PORT_D))
    time.sleep(4)

def rotate_right(alpha):
    #alpha = angle in radians
    encoder_value = int(alpha*AXIS_RADIUS* 180/(np.pi * WHEEL_RADIUS))
    BP.set_motor_position(BP.PORT_A, -encoder_value)
    BP.set_motor_position(BP.PORT_D, encoder_value)
    BP.offset_motor_encoder(BP.PORT_A, BP.get_motor_encoder(BP.PORT_A))
    BP.offset_motor_encoder(BP.PORT_D, BP.get_motor_encoder(BP.PORT_D))
    time.sleep(4)

#given the robot’s current estimated location (x, y, θ),
#drives it to the waypoint at (Wx, Wx) specified in metre units
def naviagteToWaypoint(target_x, target_y):
    global CURRENT_X, CURRENT_Y, CURRENT_THETA
    displacement_x = target_x - CURRENT_X
    displacement_y = target_y - CURRENT_Y

    print("displacement_x", displacement_x)
    print("displacement_y", displacement_y)
    displacement_theta = math.atan(displacement_y / (displacement_x + 0.000001))
    #run
    target_theta = displacement_theta - CURRENT_THETA
    target_distance = math.sqrt(displacement_x**2 + displacement_y**2)

    #fist quadrant
    if(displacement_x>=0 and displacement_y>0): 
        if target_theta < np.pi:
            rotate_left(target_theta * K_T)
        else:
            rotate_right((2 * np.pi - target_theta) * K_T)

        CURRENT_THETA += target_theta
        print("targey", target_theta)
        print("current",CURRENT_THETA)


    #third quadrant
    elif(displacement_x<0 and displacement_y<=0):
        if (np.pi-target_theta) < np.pi: 
            rotate_right((np.pi-target_theta) * K_T)
        else:
            rotate_left((2 * np.pi - (np.pi-target_theta)) * K_T)

        CURRENT_THETA -= (np.pi-target_theta)
        print("targey", target_theta)
        print("current",CURRENT_THETA)


    #second quadrant
    elif(displacement_x<0 and displacement_y>=0):
        if (np.pi+target_theta) < np.pi:
            rotate_left((np.pi+target_theta) * K_T)
        else:
            rotate_right((2* np.pi - (np.pi+target_theta)) * K_T)

        CURRENT_THETA += (np.pi+target_theta)
        print("targey", target_theta)
        print("current",CURRENT_THETA)


    #fourth quadrant
    elif(displacement_x>=0 and displacement_y<0):
        if (-target_theta) < np.pi:
            rotate_right(-(target_theta * K_T))
        else:
            rotate_left((2 * np.pi + target_theta) * K_T)
        CURRENT_THETA += target_theta
        print("targey", target_theta)
        print("current",CURRENT_THETA)


    # step  = target_distance // 20
    # remainder = target_distance % 20
    
    # if remainder > 5:
    #     remainder = remainder * 1.07

    move_forward(target_distance * K_F)
    # for i in range(int(step)):
    #     move_forward(20 * K_F)
    #     time.sleep(2)
    # move_forward(remainder*0.95)

    time.sleep(2)
    print("target_distance", target_distance)
    print("current theta", CURRENT_THETA)


    CURRENT_X += target_distance * math.cos(CURRENT_THETA)


    CURRENT_Y += target_distance * math.sin(CURRENT_THETA)
    print("current_x", CURRENT_X)
    print("current_y", CURRENT_Y)



BP.set_motor_position_kp(BP.PORT_A,25)
BP.set_motor_position_kd(BP.PORT_A,70)
BP.set_motor_limits(BP.PORT_A,250,300)

BP.set_motor_position_kp(BP.PORT_D,25)
BP.set_motor_position_kd(BP.PORT_D,70)
BP.set_motor_limits(BP.PORT_D,250,300)

naviagteToWaypoint(96,0)
time.sleep(2)
naviagteToWaypoint(96,24)   
time.sleep(2)
naviagteToWaypoint(54,24) 
time.sleep(2)
naviagteToWaypoint(54,138)
time.sleep(2)
naviagteToWaypoint(30,138) 
time.sleep(2)
naviagteToWaypoint(30,54) 
time.sleep(2)
naviagteToWaypoint(0,54) 
time.sleep(2)
naviagteToWaypoint(0,0) 



