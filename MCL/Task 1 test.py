from __future__ import print_function # use python 3 syntax but make it compatible with python 2
from __future__ import division      #                          ''

import numpy as np
import time     # import the time library for the sleep function
import brickpi3 # import the BrickPi3 drivers
import random
import math
import copy

BP = brickpi3.BrickPi3()

ORIGIN = (0,0,0)
NUMBER_OF_PARTICLES = 100
PARTICLE_UPDATED = []
PARTICLE_HISTORY = []
WEIGHTS = []

O_x = 0
O_y = 0
A_x = 0
A_y = 168
B_x = 84
B_y = 168
C_x = 84
C_y = 126
D_x = 85
D_y = 210
E_x = 168
E_y = 210
F_x = 168
F_y = 84
G_x = 210 
G_y = 84
H_x = 210
H_y = 0

O = (O_x,O_y)
A = (A_x,A_y)
B = (B_x,B_y)
C = (C_x,C_y)
D = (D_x,D_y)
E = (E_x,E_y)
F = (F_x,F_y)
G = (G_x,G_y)
H = (H_x,H_y)

std_s = 1

def get_sonar_value():
    try:
        value = BP.get_sensor(BP.PORT_3)
        print(value)                         
    except brickpi3.SensorError as error:
            print(error)
    time.sleep(1) 
    
    return value


def particle_initialization():
    for i in range(NUMBER_OF_PARTICLES):
        PARTICLE_UPDATED.append(ORIGIN)
        WEIGHTS.append(1/NUMBER_OF_PARTICLES)

def cal_m(A_x, A_y, B_x, B_y, x, y, theta):
    m_nominator = (B_y - A_y)*(A_x - x) - (B_x - A_x)*(A_y - y)
    m_denominator = (B_y - A_y)*math.cos(theta) - (B_x - A_x)*math.sin(theta)
    return m_nominator/m_denominator

def world_val(x,y,theta,m):
    x += m * math.cos(theta)
    y += m * math.sin(theta)
    return(x,y)

def wall_identification(x,y):
    if(x == O_x and O_y <= y < A_y): 
        return (O_x,O_y,A_x,A_y)
    if(y == A_y and A_x <= x < B_x):
        return (A_x,A_y,B_x,B_y)
    if(x == C_x and C_y <= y <= D_y):
        return (C_x,C_y,D_x,D_y)
    if(y == D_y and D_x < x <= E_x):
        return (D_x,D_y,E_x,E_y)
    if(x == F_x and F_y <= y < E_y):
        return (F_x,F_y,E_x,E_y)
    if(y == F_y and F_x < x <= G_x):
        return (F_x,F_y,G_x,G_y)
    if (x == H_x and H_y <= y < G_y):
        return (H_x,H_y,G_x,G_y)
    if (y == O_y and O_x < x < H_x):
        return (O_x,O_y,H_x,H_y)

def calculate_likelihood(x,y,theta,z):
    m = cal_m(wall_identification(x,y)[0],wall_identification(x,y)[1],wall_identification(x,y)[2],wall_identification(x,y)[3],x,y,theta)
    likelihood = math.exp(-(z-m)**2 / 2*(std_s**2))
    return likelihood

def update_weights(weight_list, particle_list, z):
    for i in range(len(weight_list)):
        weight_list[i] = weight_list[i] * calculate_likelihood(particle_list[i][0], particle_list[i][1], particle_list[i][2], z)
    return weight_list

def forward_update_particle(particle, distance):
    print("status:", BP.get_motor_status(BP.PORT_A))
    print("distance:", distance)

    # line = []
    for i in range(NUMBER_OF_PARTICLES):
        e = random.gauss(mu = 0, sigma = 0.1)
        f = random.gauss(mu = 0, sigma = 0.02)
        PARTICLE_UPDATED[i] = (particle[i][0]+(distance + e) * math.cos(particle[i][2]), particle[i][1]+(distance + e) * math.sin(particle[i][2]), particle[i][2]+f)

    return PARTICLE_UPDATED

def turn_update_particles(particle, angle):
    for i in range(NUMBER_OF_PARTICLES):
        g = random.gauss(mu = 0, sigma = 0.1)
        PARTICLE_UPDATED[i] = (particle[i][0], particle[i][1], particle[i][2]+(angle + g))
   

def weight_normalize(weight_list):
    #normalize weight
    sum_of_weight = 0
    for i in len(weight_list):
        sum_of_weights += weight_list[i]
    for i in len(weight_list):
        weight_list[i] /= sum_of_weight
    return weight_list

# Task 2
def resampled_particles(partcile_list, weight_list):
    resampled_particles = []
    resampled_indices = np.random.choice(len(partcile_list), size=len(partcile_list), replace=True, p=weight_list)
    for i in resampled_indices:
        resampled_particles.append(partcile_list[i])

    # Reset weights to be uniform
    for i in len(weight_list):
        weight_list[i] = 1.0 / len(resampled_particles)

    return resampled_particles

#Task 3
def particle_predicted(particle_list, weight_list_normal):
    sum = 0
    for i in range(len(particle_list)):
        sum += particle_list[i] * weight_list_normal[i]



        #1.Particle initialization 
        #2.Forward_update_particle / Turn_update_particle
        #3.Get_sonar_value (get value z)
        #4.Calculate value m
        #5.world_val 
        #6.Wall identification
        #7.Calculate likelihood 
        #8.Update weights
        #9.Weight normalization 
        #10.Resampled
        #Loop to step 2

particle_initialization()
forward_update_particle(PARTICLE_UPDATED,20)
z = get_sonar_value()