#!/usr/bin/env python3

import time
import sys
from common import *

MM_DISTANCE = float(sys.argv[1])

BP.reset_motor_encoder(PORT_B)
BP.reset_motor_encoder(PORT_C)

set_limit_at(35)

move(MM_DISTANCE)
