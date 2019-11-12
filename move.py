#!/usr/bin/env python3

import time
import sys
from common import *

MM_DISTANCE = float(sys.argv[1])

reset_encoders()

move(MM_DISTANCE)

print("Move complete")
