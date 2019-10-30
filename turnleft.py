#!/usr/bin/env python3

import time
import sys
from common import *

degrees = float(sys.argv[1])

BP.reset_motor_encoder(BP.PORT_B)
BP.reset_motor_encoder(BP.PORT_C)

BP.set_motor_limits(BP.PORT_B, 25)
BP.set_motor_limits(BP.PORT_C, 25)

turn_left(degrees)
