#!/usr/bin/env python3

import time
from rendering import *
from localisation import *

drawCoordinateFrame(1)

NINETY = 3.1415 / -2
points = PointCloud(10, 50, 0)
#print(points.get_mean())

for x in range(0, 4):
  drawParticlesStateful(points)
  points.move(10)
  time.sleep(0.25)
points.rotate(NINETY)
for x in range(0, 4):
  drawParticlesStateful(points)
  points.move(10)
  time.sleep(0.25)
points.rotate(NINETY)
for x in range(0, 4):
  drawParticlesStateful(points)
  points.move(10)
  time.sleep(0.25)
points.rotate(NINETY)
for x in range(0, 4):
  drawParticlesStateful(points)
  points.move(10)
  time.sleep(0.25)
drawParticlesStateful(points)
