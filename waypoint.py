#!/usr/bin/env python3

import time
import common
import mcl

from localisation import PointCloud
from rendering import *
from math import atan2, cos, sin, degrees, radians, sqrt, hypot, pi
from debug import *

WAIT_AFTER_MOVE_TIME = 0.3
USING_MCL = True


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
    time.sleep(WAIT_AFTER_MOVE_TIME)


def compute_delta_angle_and_distance(cur_x_cm, cur_y_cm, target_x_cm, target_y_cm, current_angle_radians):
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


def ROBOT_rotate_left_radians(delta_angle_radians):
    ROBOT_rotate_left(degrees(delta_angle_radians))


def ROBOT_move_forward(delta_cm):
    global points
    #common.move_cm(distance, lambda delta: (points.move(delta), points.fuse_sonar(common.get_sonar_cm()), drawParticles(points)))
    common.move_cm(delta_cm)
    points.move(delta_cm)


def ROBOT_move_forward_with_bump_check(delta_cm):
    global points
    distance_moved_cm = common.move_cm_check_bumps(delta_cm)
    print("MOVED", distance_moved_cm)
    #
    #
    #
    # TODO: BUMPING MCL
    #
    #
    #
    points.move(distance_moved_cm)
    points.rotate_degrees_left(180)
    ROBOT_update_estimated_position_using_mcl_and_sonar()



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


def navigate_to_waypoint_cm(target_x_cm, target_y_cm):
    global x_cm, y_cm, angle_radians, points
    DEBUG_print_current_state_rad(x_cm, y_cm, angle_radians)

    (delta_angle_degrees, distance_to_travel_cm) = compute_delta_angle_and_distance(x_cm, y_cm, target_x_cm, target_y_cm, angle_radians)
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


def ROBOT_initialize_waypoint_state(init_x_cm, init_y_cm, init_angle_radians):
    global x_cm, y_cm, angle_radians, points
    x_cm = init_x_cm
    y_cm = init_y_cm
    angle_radians = init_angle_radians
    points = PointCloud(x_cm, y_cm, angle_radians)


def ROBOT_go_to_waypoint(waypoint):
    navigate_to_waypoint_cm(waypoint[0], waypoint[1])


def ROBOT_do_waypoints(waypoints_cm):
    for waypoint in waypoints_cm:
        ROBOT_go_to_waypoint(waypoint)


def get_robot_position():
    return (x_cm, y_cm, angle_radians)
