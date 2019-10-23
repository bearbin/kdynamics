import time
import sys
import brickpi3

BP = brickpi3.BrickPi3()

PORT_A = BP.PORT_A
PORT_B = BP.PORT_B
PORT_C = BP.PORT_C

class ScalingFactors:
   movement = 1.05 * 360 / 229 
   rotation = (96/90) * 0.96 * 360 / 229 

def get_motor_power(BP, port):
    return BP.get_motor_status(port)[1]
