#!/usr/bin/env python3

import time
import sys
from common import *

MM_DISTANCE = float(sys.argv[1])

reset_encoders()

set_limit_at(35)

move(MM_DISTANCE)

print("Move complete")
