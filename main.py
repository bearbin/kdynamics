#!/usr/bin/env python3

#
# This is our final executable file
#

import time
import common
import mcl
import waypoint

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


def ROBOT_do_seek_and_destroy_approach():
    ROBOT_do_route_looking_for_bottle_1()

######################## EXECUTING CODE ##########################

drawWorld()
ROBOT_initialize_waypoint_state(INITIAL_X, INITIAL_Y, INITIAL_ANGLE)


