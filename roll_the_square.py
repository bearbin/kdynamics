#!/usr/bin/env python3

import time
from rendering import *
from localisation import *
from common import *

set_limit_at(25)
drawCoordinateFrame(1)

NINETY = 3.1415 / -2
points = PointCloud(10, 50, 0)
#print(points.get_mean())

drawParticlesStateful(points)
for line in range(0, 4):
    for x in range(0, 4):
        move(100)
        points.move(10)
        drawParticlesStateful(points)
        time.sleep(0.8)
    turn_left(90)
    points.rotate(NINETY)
    time.sleep(1.8)

