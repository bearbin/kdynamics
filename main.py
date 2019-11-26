#!/usr/bin/env python3

#
# This is our final executable file
#

import time
import common
import mcl
from waypoint import *
from sweep import *

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

MAX_DESTROY_ADVANCE_CM = 1000

class Waypoints:
    class Path1:
        SEEK = [[84, 25]]
        # SEEK = [[42, 34], [42, 50]]
        RETALIATE = [INITIAL_POSITION]
        WAYPOINT_ID = 'c'
    class Path2:
        SEEK = [[90, 70]]
        RETALIATE = [INITIAL_POSITION]
        WAYPOINT_ID = 'b'
    class Path3:
        SEEK = [[90, 30]]
        RETALIATE = [INITIAL_POSITION]
        WAYPOINT_ID = 'a'

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

def SONAR_locate_target(waypoint_id):
    #
    #
    #
    # TODO: Change MCL to accout for sonar angle, or restore sonar after the seek
    #
    #
    #
    return -find_angle_rotation_robot_left(waypoint_id)


def ROBOT_seek_and_destroy(path_info):
    left_rotation_angle_radians = SONAR_locate_target(path_info.WAYPOINT_ID)

    ROBOT_rotate_left_radians(left_rotation_angle_radians)
    ROBOT_move_forward_with_bump_check(MAX_DESTROY_ADVANCE_CM)


def ROBOT_destroy(path_info):
    waypoints_to_seek = path_info.SEEK
    waypoints_to_retaliate = path_info.RETALIATE

    ROBOT_do_waypoints(waypoints_to_seek)
    ROBOT_seek_and_destroy(path_info)
    ROBOT_do_waypoints(waypoints_to_retaliate)


def ROBOT_destroy_first():
    ROBOT_destroy(Waypoints.Path1)


def ROBOT_destroy_second():
    ROBOT_destroy(Waypoints.Path2)


def ROBOT_destroy_third():
    ROBOT_destroy(Waypoints.Path3)


def ROBOT_return_to_origin():
    ROBOT_go_to_waypoint(INITIAL_POSITION)


def ROBOT_do_seek_and_destroy_approach():
    ROBOT_destroy_first()
    ROBOT_destroy_second()
    ROBOT_destroy_third()
    ROBOT_return_to_origin()

######################## EXECUTING CODE ##########################

drawWorld()
ROBOT_initialize_waypoint_state(INITIAL_X, INITIAL_Y, INITIAL_ANGLE)

ROBOT_do_seek_and_destroy_approach()
