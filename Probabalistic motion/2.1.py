from __future__ import print_function # use python 3 syntax but make it compatible with python 2
from __future__ import division      #                          ''

import numpy as np
import time     # import the time library for the sleep function
import brickpi3 # import the BrickPi3 drivers
import random
import math
import copy

BP = brickpi3.BrickPi3() # Create an insta


WHEEL_RADIUS = 2.8
AXIS_RADIUS = 6.6

NUMBER_OF_PARTICLES = 100
WEIGHT = 1/NUMBER_OF_PARTICLES 
ORIGIN = (0,0,0)
START = (200,600,0)
ANGLE = np.pi/2
PARTICLE_UPDATED = []
PARTICLE_HISTORY = []
SCALED_PARTICLE = []
SCALED_HISTORY = []
SCALED_PARTICLE_TURN = []




K = 10
U_0 = 200
V_0 = 600

def move_forward(distance):
    encoder_value = int(distance * 180/(np.pi * WHEEL_RADIUS))
    BP.set_motor_position(BP.PORT_A, encoder_value)
    BP.set_motor_position(BP.PORT_D, encoder_value)
    BP.offset_motor_encoder(BP.PORT_A, BP.get_motor_encoder(BP.PORT_A))
    BP.offset_motor_encoder(BP.PORT_D, BP.get_motor_encoder(BP.PORT_D))
    time.sleep(3)

def rotate(alpha):
    #alpha = angle in radians
    encoder_value = int(alpha*AXIS_RADIUS* 180/(np.pi * WHEEL_RADIUS))
    BP.set_motor_position(BP.PORT_A, encoder_value)
    print(encoder_value)
    BP.set_motor_position(BP.PORT_D, -encoder_value)
    BP.offset_motor_encoder(BP.PORT_A, BP.get_motor_encoder(BP.PORT_A))
    BP.offset_motor_encoder(BP.PORT_D, BP.get_motor_encoder(BP.PORT_D))
    time.sleep(3)

# PARTICLE should be (x, y , theta) update single point
def particle_initialization():
    for i in range(NUMBER_OF_PARTICLES):
        PARTICLE_UPDATED.append(ORIGIN)
        SCALED_HISTORY.append(ORIGIN)
        SCALED_PARTICLE.append(ORIGIN)
        SCALED_PARTICLE_TURN.append(ORIGIN)

def forward_update_particle(particle):
    print("status:", BP.get_motor_status(BP.PORT_A))
    # distance = (np.abs(BP.get_motor_encoder(BP.PORT_A)) + np.abs(BP.get_motor_encoder(BP.PORT_D))) / 360 * np.pi *2.8
    distance = 15
    print("distance:", distance)

    history = copy.deepcopy(particle)
    x_history_mean = 0
    y_history_mean = 0
    x_update_mean = 0
    y_update_mean = 0
    line = []
    for i in range(NUMBER_OF_PARTICLES):
        e = random.gauss(mu = 0, sigma = 0.1)
        f = random.gauss(mu = 0, sigma = 0.02)
        PARTICLE_UPDATED[i] = (particle[i][0]+(distance + e) * math.cos(particle[i][2]), particle[i][1]+(distance + e) * math.sin(particle[i][2]), particle[i][2]+f)
        SCALED_HISTORY[i] = (K*history[i][0] + U_0, V_0 - K* history[i][1], history[i][2])
        x_history_mean += SCALED_HISTORY[i][0]
        y_history_mean += SCALED_HISTORY[i][1]
    
    for i in range(NUMBER_OF_PARTICLES):
        SCALED_PARTICLE[i] = (K*PARTICLE_UPDATED[i][0] + U_0, V_0 - K*PARTICLE_UPDATED[i][1], PARTICLE_UPDATED[i][2])
        x_update_mean += SCALED_PARTICLE[i][0]
        y_update_mean += SCALED_PARTICLE[i][1]

    line.append((x_history_mean/ NUMBER_OF_PARTICLES,y_history_mean / NUMBER_OF_PARTICLES,x_update_mean / NUMBER_OF_PARTICLES,y_update_mean / NUMBER_OF_PARTICLES))
    print("drawParticles:" + str(SCALED_PARTICLE))
    print("drawLine:" + str(line))

    return PARTICLE_UPDATED


def turn_update_particles(particle):
    for i in range(NUMBER_OF_PARTICLES):
        g = random.gauss(mu = 0, sigma = 0.1)
        PARTICLE_UPDATED[i] = (particle[i][0], particle[i][1], particle[i][2]+(ANGLE + g))
    for i in range(NUMBER_OF_PARTICLES):
        SCALED_PARTICLE_TURN[i] = (K*PARTICLE_UPDATED[i][0] + U_0, V_0 - K*PARTICLE_UPDATED[i][1], PARTICLE_UPDATED[i][2])

    print("drawParticles:" + str(SCALED_PARTICLE_TURN))

    

def run():
    BP.set_motor_position_kp(BP.PORT_A,25)
    BP.set_motor_position_kd(BP.PORT_A,70)
    BP.set_motor_limits(BP.PORT_A,200,250)

    BP.set_motor_position_kp(BP.PORT_D,25)
    BP.set_motor_position_kd(BP.PORT_D,70)
    BP.set_motor_limits(BP.PORT_D,200,250)

    print("drawParticles:" + str(START))
    particle_initialization()
    
    for i in range(4):
        print("Run #:", i)
        print("Encoder positions:")
        print(BP.get_motor_encoder(BP.PORT_A),BP.get_motor_encoder(BP.PORT_D))

        for i in range(4):
            print('Move forward : ', (i+1))
            PARTICLE_HISTORY = PARTICLE_UPDATED
            move_forward(15)
            forward_update_particle(PARTICLE_UPDATED)

            print(BP.get_motor_encoder(BP.PORT_A),BP.get_motor_encoder(BP.PORT_D))

        rotate(np.pi/2 * 1.02)
        turn_update_particles(PARTICLE_UPDATED)
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