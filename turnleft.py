#!/usr/bin/env python3

import time
import sys
from common import *

degrees = float(sys.argv[1])

try:
	turn_left(degrees)
finally:
	total_reset()
