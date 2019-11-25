#!/usr/bin/env python3

import time
import sys
from common import *

reset_encoders()

try:
  while True:
    bumped = check_bump()
    if bumped != BumpStatus.NONE:
        print(bumped)
except KeyboardInterrupt:
	total_reset()

