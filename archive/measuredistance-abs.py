#!/usr/bin/env python3

import time
import sys
from common import *

MM_DISTANCE = float(sys.argv[1])

BP.reset_motor_encoder(BP.PORT_B)
BP.reset_motor_encoder(BP.PORT_C)

BP.set_motor_position_kd(BP.PORT_B, 95)
BP.set_motor_position_kd(BP.PORT_C, 95)
BP.set_motor_position_kp(BP.PORT_B, 75)
BP.set_motor_position_kp(BP.PORT_C, 75)

BP.set_motor_limits(BP.PORT_B, 35)
BP.set_motor_limits(BP.PORT_C, 35)

final_encoder_pos = ScalingFactors.movement * MM_DISTANCE

BP.set_motor_position(BP.PORT_B, final_encoder_pos)
BP.set_motor_position(BP.PORT_C, final_encoder_pos)

time.sleep(3)
