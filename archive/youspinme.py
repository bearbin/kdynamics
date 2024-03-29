#!/usr/bin/env python3

import time
import sys
from common import *

try:
    POWER = int(sys.argv[1])
    try:
        USE_DPS = bool(sys.argv[2])
    except:
        USE_DPS = False

    BP = brickpi3.BrickPi3()

    func = BP.set_motor_dps if USE_DPS else BP.set_motor_power

    SPIN_FACTOR = 1.41
    func(BP.PORT_A, POWER/(SPIN_FACTOR))
    func(BP.PORT_B, POWER)
    func(BP.PORT_C, -POWER)
except:
    BP.reset_all()

# scaling_factor = 360/220
# MM_DISTANCE = int(sys.argv[1])
# scaled_distance = MM_DISTANCE * scaling_factor

# encoder_b_position = 0
# encoder_c_position = 0
# while True:
#     encoder_b_position += BP.get_motor_encoder(BP.PORT_B)
#     encoder_c_position += BP.get_motor_encoder(BP.PORT_C)
#     BP.reset_motor_encoder(BP.PORT_B)
#     BP.reset_motor_encoder(BP.PORT_C)

#     print(encoder_b_position, encoder_c_position)

#     if encoder_b_position > scaled_distance:
#         BP.set_motor_power(BP.PORT_B, 0)
#     if encoder_c_position > scaled_distance:
#         BP.set_motor_power(BP.PORT_C, 0)
#     if (get_motor_power(BP.PORT_B) == 0 and get_motor_power(BP.PORT_C) == 0):
#         break
#     time.sleep(0.02)

