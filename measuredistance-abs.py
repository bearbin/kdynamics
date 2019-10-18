#!/usr/bin/env python3

import time
import sys
import brickpi3

MM_DISTANCE = float(sys.argv[1])
scaling_factor = 360/229
scaled_distance = abs(MM_DISTANCE * scaling_factor)

def get_motor_power(port):
    return BP.get_motor_status(port)[1]

BP = brickpi3.BrickPi3()

BP.reset_motor_encoder(BP.PORT_B)
BP.reset_motor_encoder(BP.PORT_C)

BP.set_motor_limits(BP.PORT_B, 35)
BP.set_motor_limits(BP.PORT_C, 35)

BP.set_motor_position(BP.PORT_B, scaling_factor * MM_DISTANCE)
BP.set_motor_position(BP.PORT_C, scaling_factor * MM_DISTANCE)


