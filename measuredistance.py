#!/usr/bin/env python3

import time
import sys
import brickpi3

scaling_factor = 360/220

BP = brickpi3.BrickPi3()
BP.set_motor_power(BP.PORT_B, 40)
BP.set_motor_power(BP.PORT_C, 40)

encoder_b_position = 0
encoder_c_position = 0
while True:
    encoder_b_position += BP.get_motor_encoder(BP.PORT_B)
    encoder_c_position += BP.get_motor_encoder(BP.PORT_C)
    BP.reset_motor_encoder(BP.PORT_B)
    BP.reset_motor_encoder(BP.PORT_C)
    if encoder_b_position > int(sys.argv[1]) * scaling_factor:
        BP.set_motor_power(BP.PORT_B, 0)
    if encoder_c_position > int(sys.argv[1]) * scaling_factor:
        BP.set_motor_power(BP.PORT_C, 0)
    if (BP.get_motor_status(BP.PORT_B)[1] == 0 and BP.get_motor_status(BP.PORT_C)[1] == 0):
        break
    time.sleep(0.02)
