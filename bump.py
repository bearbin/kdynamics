#!/usr/bin/env python3

import time
import sys
from common import *

reset_encoders()
set_sensors()

try:
  move_cm_check_bumps(100)
  while True:
    bumped = check_bump()
    if bumped != BumpStatus.NONE:
        print(bumped)
except KeyboardInterrupt:
	total_reset()

