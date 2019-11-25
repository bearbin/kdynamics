#!/usr/bin/env python3

import time
import common
import mcl

from localisation import PointCloud
from rendering import *
from math import atan2, cos, sin, degrees, radians, sqrt, hypot, pi

WAIT_TIME = 0.5
USING_MCL = True

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

def compute_clamped_delta(target_angle_radians, current_angle_radians):
    delta_angle_radians = (target_angle_radians - current_angle_radians)
    if delta_angle_radians <= -pi:
      delta_angle_radians += 2 * pi
    elif delta_angle_radians > pi:
      delta_angle_radians -= 2 * pi
    return delta_angle_radians

def compute_target_angle_radians(delta_x, delta_y):
    return atan2(delta_y, delta_x) 

def wait():
    time.sleep(WAIT_TIME)

def compute_delta_angle_and_distance(cur_x_cm, cur_y_cm, target_x_cm, target_y_cm):
    delta_y_cm = target_y_cm - cur_y_cm
    delta_x_cm = target_x_cm - cur_x_cm

    target_angle_radians = compute_target_angle_radians(delta_x_cm, delta_y_cm)
    delta_angle_radians = compute_clamped_delta(target_angle_radians, current_angle_radians)
    delta_angle_degrees = degrees(delta_angle_radians)
    distance_to_travel_cm = hypot(delta_x_cm, delta_y_cm)

    DEBUG_print_target_state_rad(target_x_cm, target_y_cm, target_angle_radians)
    DEBUG_print_delta_state_rad(delta_x_cm, delta_y_cm, delta_angle_radians)

    return (delta_angle_degrees, distance_to_travel_cm)


def ROBOT_rotate_left(delta_angle_degrees):
    global points
    common.turn_left(delta_angle_degrees)
    points.rotate_degrees_left(delta_angle_degrees)


def ROBOT_move_forward(delta_cm):
    global points
    #common.move_cm(distance, lambda delta: (points.move(delta), points.fuse_sonar(common.get_sonar_cm()), drawParticles(points)))
    common.move_cm(delta_cm)
    points.move(delta_cm)


def ROBOT_set_estimated_position(new_x_cm, new_y_cm, new_angle_radians):
    global x_cm, y_cm, angle_radians, points
    x_cm = new_x_cm
    y_cm = new_y_cm
    angle_radians = new_angle_radians


def ROBOT_update_estimated_position_using_mcl_and_sonar():
    global x_cm, y_cm, angle_radians, points

    sonar_reading_cm = common.get_sonar_cm()
    points.fuse_sonar(sonar_reading_cm)
    new_mean = points.get_mean()

    x_cm = new_mean.x
    y_cm = new_mean.y
    angle_radians = common.normalise_rads(new_mean.angle)


def mcl_redraw():
    global points
    drawParticlesStateful(points)


def navigate_to_waypoint_cm(target_x_cm, target_y_cm)
    global x_cm, y_cm, angle_radians, points
    DEBUG_print_current_state_deg(x_cm, y_cm, angle_radians)

    (delta_angle_degrees, distance_to_travel_cm)
      = compute_delta_angle_and_distance(x_cm, y_cm, target_x_cm, target_y_cm)
    
    if (distance_to_travel_cm == 0):
        return

    ROBOT_rotate_left(delta_angle_degrees)
    wait()

    ROBOT_move_forward(distance_to_travel_cm)
    wait()

    if USING_MCL:
        ROBOT_update_estimated_position_using_mcl_and_sonar()
    else:
        ROBOT_set_estimated_position(target_x_cm, target_y_cm, angle_radians + delta_angle_degrees)


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

