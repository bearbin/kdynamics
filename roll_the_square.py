#!/usr/bin/env python3

import time
from rendering import *
from localisation import *
from common import *

reset_encoders()
set_limit_at(25)
drawCoordinateFrame(1)

points = PointCloud(0, 0, 0)
print(points.get_mean())

drawParticles(points)
for line in range(0, 4):
    for x in range(0, 4):
        move(100)
        points.move(10)
        resetDrawingState()
        drawParticles(points)
        print("The mean is: ", points.get_mean())
        time.sleep(1)  # Pause after a little step 
    turn_left(90)
    points.rotate_degrees_left(90)
    time.sleep(1.8)
    resetDrawingState()
    drawParticles(points)

