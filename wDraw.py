#!/usr/bin/env python3

import time
from rendering import *
from localisation import *
from common import *


points = [(0,x/2.5,10,x/100) for x in range(100)]
drawParticlesStateful(points)
points = [(2,x/2.5,10,x/100) for x in range(100)]


drawParticlesStateful(points)
drawParticlesStateful(points)
drawParticlesStateful(points)
drawParticlesStateful(points)
drawParticlesStateful(points)
