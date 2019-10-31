#!/usr/bin/env python3

import time
from rendering import *
from localisation import *

drawCoordinateFrame(0)

for x in range(10,61):
  drawParticlesStateful([(x, x, 0.4, 1)])
  time.sleep(0.05)
