#!/usr/bin/env python3

import time
import sys
from common import *

degrees = float(sys.argv[1])

set_limit_at(20,20)

try:
  turn_top(-degrees)
  turn_left(degrees)
finally:
  total_reset()
