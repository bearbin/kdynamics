#!/usr/bin/env python3

import time
import sys
from common import *

MM_DISTANCE = float(sys.argv[1])

BP.reset_motor_encoder(PORT_B)
BP.reset_motor_encoder(PORT_C)

BP.set_motor_limits(PORT_B, 35)
BP.set_motor_limits(PORT_C, 35)

# -1 factor because big wheels at the front!
final_encoder_pos = (-1) * ScalingFactors.movement * MM_DISTANCE
stop_threshold = 0.99 * final_encoder_pos

BP.set_motor_position(PORT_B, final_encoder_pos)
BP.set_motor_position(PORT_C, final_encoder_pos)

while (abs(get_motor_position(PORT_B)) < abs(stop_threshold) and
       abs(get_motor_position(PORT_C)) < abs(stop_threshold)):
    print(get_motor_position(PORT_B))
