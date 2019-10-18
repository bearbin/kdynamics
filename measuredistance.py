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

BP.set_motor_power(BP.PORT_B, 15 * (MM_DISTANCE / abs(MM_DISTANCE)))
BP.set_motor_power(BP.PORT_C, 15 * (MM_DISTANCE / abs(MM_DISTANCE)))


BP.reset_motor_encoder(BP.PORT_B)
BP.reset_motor_encoder(BP.PORT_C)

while True:
    encoder_b_position = abs(BP.get_motor_encoder(BP.PORT_B))
    encoder_c_position = abs(BP.get_motor_encoder(BP.PORT_C))

    print(encoder_b_position, encoder_c_position)

    if encoder_b_position > scaled_distance:
        BP.set_motor_power(BP.PORT_B, 0)
    if encoder_c_position > scaled_distance:
        BP.set_motor_power(BP.PORT_C, 0)
    if (get_motor_power(BP.PORT_B) == 0 and get_motor_power(BP.PORT_C) == 0):
        break
    time.sleep(0.02)

