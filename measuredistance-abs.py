#!/usr/bin/env python3

import time
import sys
from common import *

MM_DISTANCE = float(sys.argv[1])
scaled_distance = abs(MM_DISTANCE * ScalingFactors.movement)

BP.reset_motor_encoder(BP.PORT_B)
BP.reset_motor_encoder(BP.PORT_C)

BP.set_motor_limits(BP.PORT_B, 35)
BP.set_motor_limits(BP.PORT_C, 35)

final_encoder_pos = ScalingFactors.movement * MM_DISTANCE
#for pos in range(0, int(final_encoder_pos), 20):
#    BP.set_motor_position(BP.PORT_B, pos)
#    BP.set_motor_position(BP.PORT_C, pos)

BP.set_motor_position(BP.PORT_B, final_encoder_pos)
BP.set_motor_position(BP.PORT_C, final_encoder_pos)

# TODO: wait until finished rather than waiting a time
time.sleep(5)
