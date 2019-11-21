#!/usr/bin/env python3

import time
import common
import mcl

from localisation import PointCloud
from rendering import *
from math import atan2, cos, sin, degrees, radians, sqrt, hypot, pi

WAYPOINTS = [
[84,30],

[104,30],
[124,30],
[144,30],
[164,30],

[180,30],

[180,45],

[180,54],

[160,54],

[138,54],

[138,74],
[138,94],
[138,114],
[138,134],
[138,150],

[138,168],

[126,168],

[114,168],

[114,148],
[114,128],
[114,108],

[114,84],

[94,84],

[84,84],

[84,64],
[84,44],

[84,30]
]

# NOTE: angle kept in radians, only converted to degrees for display
#       and when passed into motor functions

INITIAL_X = WAYPOINTS[0][0]
INITIAL_Y = WAYPOINTS[0][1]
INITIAL_ANGLE = 0.0

def sign(number):
    return -1 if number < 0 else 1

x_cm = INITIAL_X
y_cm = INITIAL_Y
angle = INITIAL_ANGLE
points = PointCloud(x_cm, y_cm, angle)

def normalise_rads(angle):
  return atan2(sin(angle), cos(angle))

def navigateToWaypoint(target_x_metres, target_y_metres):
    global x_cm, y_cm, angle

    common.get_sonar_cm()

    target_x_cm = target_x_metres * 100
    target_y_cm = target_y_metres * 100

    delta_y = target_y_cm - y_cm
    delta_x = target_x_cm - x_cm

    if delta_x == 0 and delta_y == 0:
      return

    target_angle = atan2(delta_y, delta_x)

    delta_angle = (target_angle - angle)
    if delta_angle <= -pi:
      delta_angle += 2 * pi
    elif delta_angle > pi:
      delta_angle -= 2 * pi

    #print()
    #print()
    #print()
    #print("I need to move in y by = ", delta_y)
    #print("I need to move in x by = ", delta_x)
    print("I need to rotate by degree angle = ", degrees(delta_angle))
    #print("Final absolute angle I need to get to = ", target_angle)
    #print("My current absolute angle = ", angle)

    common.turn_left(degrees(delta_angle))
    points.rotate_degrees_left(degrees(delta_angle))

    #time.sleep(2)

    distance = hypot(delta_x, delta_y)
    #print("Distance I need to travel = ", distance)
    #common.move_cm(distance, lambda delta: (points.move(delta), points.fuse_sonar(common.get_sonar_cm()), drawParticles(points)))
    common.move_cm(distance)
    points.move(distance)

    time.sleep(0.5)

    sonar_reading = common.get_sonar_cm()
    print("My sonar reading is ", sonar_reading)

    points.fuse_sonar(sonar_reading)
    new_mean = points.get_mean()
    angle = angle + delta_angle
    x_cm = x_cm + delta_x
    y_cm = y_cm + delta_y
#    angle = normalise_rads(new_mean.angle)
#    x_cm = new_mean.x
#    y_cm = new_mean.y
    print(x_cm, y_cm)
    print()

    drawParticlesStateful([(x_cm,y_cm,1,1)])
    # drawParticlesStateful(points)

drawCoordinateFrame(1)
drawWalls()
drawPath()

i = 0
try:
  while i < len(WAYPOINTS):
    # print("Insert WX and WY")
    # [target_x, target_y] = map(float, input().split())
    print(points.get_mean())

    [target_x, target_y] = map(lambda x: x / 100, WAYPOINTS[i])
    i = (i + 1) # % len(WAYPOINTS)
    navigateToWaypoint(target_x, target_y)
finally:
  common.total_reset()

