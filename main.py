#!/usr/bin/env python3

#
# This is our final executable file
#

import time
import common
import mcl

from localisation import PointCloud
from rendering import *
from math import atan2, cos, sin, degrees, radians, sqrt, hypot, pi

INITIAL_POSITION = [84, 30]

INITIAL_X = INITIAL_POSITION[0]
INITIAL_Y = INITIAL_POSITION[1]
INITIAL_ANGLE = 0.0

######################## EXECUTING CODE ##########################

drawWorld()