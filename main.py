#!/usr/bin/env python3

#
# This is our final executable file
#

import time
import common
import mcl
from waypoint import *

from localisation import PointCloud
from rendering import *
from math import atan2, cos, sin, degrees, radians, sqrt, hypot, pi

INITIAL_POSITION = [84, 30]

INITIAL_X = INITIAL_POSITION[0]
INITIAL_Y = INITIAL_POSITION[1]
INITIAL_ANGLE = 0.0

MIN_READING_DIFF = 10

ROUTE_1_PREPARE_WAYPOINTS = []
ROUTE_1_WAYPOINTS = []

MAX_DESTROY_ADVANCE_CM = 100

class Waypoints:
    class Path1:
        SEEK: [[100, 100]]
        RETALIATE: [[100, 100]]
    class Path2:
        SEEK: [[100, 100]]
        RETALIATE: [[100, 100]]
    class Path3:
        SEEK: [[100, 100]]
        RETALIATE: [[100, 100]]

########################## FUNCTIONS ############################

def ROBOT_do_route_looking_for_bottle_1():
    ROBOT_do_waypoints(ROUTE_1_PREPARE_WAYPOINTS)

    initial_reading = 30
    def stop_check():
        sonar_reading_cm = common.get_sonar_cm()
        return abs(initial_reading - sonar_reading_cm) > MIN_READING_DIFF

    move_cm_check_bumps_and_condition(40, stop_check)
    return


def ROBOT_do_wall_folowing_approach():
    ROBOT_do_route_looking_for_bottle_1()

##################################################################

def ROBOT_seek_and_destroy():
    left_rotation_angle_radians = SONAR_locate_target()
    ROBOT_rotate_left_radians(left_rotation_angle_radians)
    ROBOT_move_forward_with_bump_check(MAX_DESTROY_ADVANCE_CM)


def ROBOT_destroy(waypoints_to_seek, waypoints_to_retaliate):
    ROBOT_do_waypoints(waipoints_to_seek)
    ROBOT_seek_and_destroy()
    ROBOT_do_waypoints(waypoints_to_retaliate)


def ROBOT_destroy_first():
    ROBOT_destroy(Waypoints.Path1.SEEK, Waypoints.Path1.RETALIATE)


def ROBOT_destroy_second():
    ROBOT_destroy(Waypoints.Path2.SEEK, Waypoints.Path2.RETALIATE)


def ROBOT_destroy_third():
    ROBOT_destroy(Waypoints.Path3.SEEK, Waypoints.Path3.RETALIATE)


def ROBOT_do_seek_and_destroy_approach():
    ROBOT_destroy_first()
    ROBOT_destroy_second()
    ROBOT_destroy_third()
    ROBOT_return_to_origin()

######################## EXECUTING CODE ##########################

drawWorld()
ROBOT_initialize_waypoint_state(INITIAL_X, INITIAL_Y, INITIAL_ANGLE)


