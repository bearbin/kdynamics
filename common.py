import time
import sys
import brickpi3

BP = brickpi3.BrickPi3()

PORT_A = BP.PORT_A
PORT_B = BP.PORT_B
PORT_C = BP.PORT_C

class ScalingFactors:
   movement = 360 / 229 
   rotation = 0.99 * 360 / 229 

def get_motor_power(BP, port):
    return BP.get_motor_status(port)[1]