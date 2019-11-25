#!/usr/bin/env python3

import time
import sys
from common import *

MM_DISTANCE = float(sys.argv[1])

reset_encoders()


try:
    while True:
        check_bump()
finally:
	total_reset()

print("Move complete")
