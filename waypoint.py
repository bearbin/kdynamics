#!/usr/bin/env python3

import time
import common
import mcl

from localisation import PointCloud
from rendering import *
from math import atan2, cos, sin, degrees, radians, sqrt, hypot, pi

#WAYPOINTS = [
#[84,30],

#[104,30],
#[124,30],
#[144,30],
#[164,30],

#[180,30],

#[180,45],

#[180,54],

#[160,54],

#[138,54],

#[138,74],
#[138,94],
#[138,114],
#[138,134],
#[138,150],

#[138,168],

#[126,168],

#[114,168],

#[114,148],
#[114,128],
#[114,108],

#[114,84],

#[94,84],

#[84,84],

#[84,64],
#[84,44],

#[84,30]
#]


# NOTE: angle kept in radians, only converted to degrees for display
#       and when passed into motor functions
INITIAL_X = 84
INITIAL_Y = 30
INITIAL_ANGLE_RADIANS = 0.0

x_cm = INITIAL_X
y_cm = INITIAL_Y
angle_radians = INITIAL_ANGLE_RADIANS
points = PointCloud(x_cm, y_cm, angle_radians)

def sign(number):
    return -1 if number < 0 else 1

def no_need_to_move(delta_x, delta_y):
    return delta_x == 0 and delta_y == 0

def compute_clamped_delta(target_angle_radians, current_angle_radians):
    delta_angle_radians = (target_angle_radians - current_angle_radians)
    if delta_angle_radians <= -pi:
      delta_angle_radians += 2 * pi
    elif delta_angle_radians > pi:
      delta_angle_radians -= 2 * pi
    return delta_angle_radians

def compute_target_angle_radians(delta_x, delta_y):
    return atan2(delta_y, delta_x) 

def navigate_to_waypoint_cm(target_x_cm, target_y_cm)
    global x_cm, y_cm, angle_radians

    DEBUG_print_current_state_deg(x_cm, y_cm, angle_radians)

    delta_y_cm = target_y_cm - y_cm
    delta_x_cm = target_x_cm - x_cm
    if no_need_to_move(delta_x_cm, delta_y_cm):
      return

    target_angle_radians = compute_target_angle_radians(delta_x_cm, delta_y_cm)
    delta_angle_radians = compute_clamped_delta(target_angle_radians, current_angle_radians)

    

    print("I need to rotate by degree angle = ", degrees(delta_angle_radians))
    common.turn_left(degrees(delta_angle_radians))
    points.rotate_degrees_left(degrees(delta_angle_radians))

    time.sleep(0.5)

    distance = hypot(delta_x_cm, delta_y_cm)
    #print("Distance I need to travel = ", distance)
    #common.move_cm(distance, lambda delta: (points.move(delta), points.fuse_sonar(common.get_sonar_cm()), drawParticles(points)))
    print("Moving distance ", distance)
    common.move_cm(distance)
    #points.move(distance)

    time.sleep(0.5)

    #sonar_reading = common.get_sonar_cm()
   # print("My sonar reading is ", sonar_reading)

    #points.fuse_sonar(sonar_reading)
    #new_mean = points.get_mean()
    angle_radians = angle_radians + delta_angle_radians
    x_cm = x_cm + delta_x_cm
    y_cm = y_cm + delta_y_cm
   # angle_radians = normalise_rads(new_mean.angle)
   # x_cm = new_mean.x
   # y_cm = new_mean.y
   # print(x_cm, y_cm)
   # print()

    #drawParticlesStateful(points)


def navigateToWaypoint(target_x_metres, target_y_metres):
    navigate_to_waypoint_cm(target_x_metres * 100, target_y_metres * 100)

#i = 0
#try:
#  while i < len(WAYPOINTS):
    # print("Insert WX and WY")
    # [target_x, target_y] = map(float, input().split())
#    print(points.get_mean())

#    [target_x, target_y] = map(lambda x: x / 100, WAYPOINTS[i])
#    i = (i + 1) # % len(WAYPOINTS)
#    navigateToWaypoint(target_x, target_y)
#finally:
#  common.total_reset()

