
from __future__ import print_function 
from __future__ import division 
import time    
import brickpi3

BP = brickpi3.BrickPi3()
import numpy as np

BP.set_sensor_type(BP.PORT_1, BP.SENSOR_TYPE.TOUCH)
