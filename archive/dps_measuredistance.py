#!/usr/bin/env python3

import time
import sys
import brickpi3

def get_motor_power(port):
    return BP.get_motor_status(port)[1]

BP = brickpi3.BrickPi3()
BP.reset_encoder_position(
BP.set_motor_dps(BP.PORT_B, 65)
BP.set_motor_dps(BP.PORT_C, 65)

scaling_factor = 360/229
MM_DISTANCE = int(sys.argv[1])
scaled_distance = MM_DISTANCE * scaling_factor

encoder_b_position = 0
encoder_c_position = 0
while True:
    encoder_b_position += BP.get_motor_encoder(BP.PORT_B)
    encoder_c_position += BP.get_motor_encoder(BP.PORT_C)
    BP.reset_motor_encoder(BP.PORT_B)
    BP.reset_motor_encoder(BP.PORT_C)

    print(encoder_b_position, encoder_c_position)

    if encoder_b_position > scaled_distance:
        BP.set_motor_power(BP.PORT_B, 0)
        BP.set_motor_power(BP.PORT_C, 0)
    if (get_motor_power(BP.PORT_B) == 0 and get_motor_power(BP.PORT_C) == 0):
        # break
        pass
    time.sleep(0.02)

