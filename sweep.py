#!/usr/bin/env python3

import time
from common import *
from waypoint import *
from math import radians


SONAR_ROTATION_WAIT = 0.6

# Sigs are: (start angle, end_angle, dists at 5 degree intervals)

bottleless_a = (45, -45, [])

bottleless_b = (100, 0, [])

# TODO: write specific waypoint
bottleless_c = (45, -45, [43, 44, 138, 138, 137, 136, 136, 135, 134, 134, 134, 134, 133, 134, 134, 134, 134, 135, 135, 142, 143, 143, 144]   )

SWEEP_STEP_DEGREES = 5

class SweepData:
    class A:
        SWEEP_ANGLE = 45
    class B:
        SWEEP_ANGLE = 45
    class C:
        SWEEP_ANGLE = 45

def measure_sonar():
    reading = get_sonar_cm()
    print("Sonar reading was " + str(readings))
    time.sleep(0.02)
    return reading


def correct_sonar_turn(turn):
    return turn * 7.5 / 9


BP.set_motor_limits(PORT_A, 25)


def SONAR_rotate_left_degrees(angle_degrees):
    turn_sonar_left(angle_degrees)
    time.sleep(SONAR_ROTATION_LEFT)


def SONAR_record_into(readings):
    reading = measure_sonar()
    readings.append(reading)



def compute_sweep_steps_num(sweep_angle_degrees, sweep_step_degrees):
    return sweep_angle_degrees / sweep_step_degrees


def SONAR_perform_sweep_and_get_readings(sweep_angle_degrees):
    sweep_steps_num = compute_sweep_steps_num(sweep_angle_degrees, SWEEP_STEP_DEGREES)

    readings = []

    for angle_degrees in range(sweep_steps_num):
        SONAR_record_into(readings)
        SONAR_rotate_left_degrees(-SWEEP_STEP_DEGREES)
    record_sonar_into(readings)

    return readings


def compute_estimated_ideal_sonar_readings():
    return bottleless_c


def find_bottle_angle(actual_sonar_readings):
#   waypoints = []
#   threshold = 15
#   minimum_measurement = 20

#   for i in range(len(readings)):
#     if readings[i] < minimum_measurement:
#       continue
#     difference = bottleless_dists[i] - readings[i]
#     if difference >= threshold:
#       waypoints.append((180 - correct_sonar_turn(i * 5), readings[i]))

#   print("Waypoints index are ", waypoints)
#   bottle_pos = sorted(waypoints)[round(len(waypoints)/2)]
#   print("Bottle at : ", bottle_pos)
    estimated_ideal_sonar_readings = compute_estimated_ideal_sonar_readings()
    return 0


def SONAR_perform_sweep_and_get_target_angle_radians(sweep_data):
  sweep_angle_degrees = sweep_data.SWEEP_ANGLE

  SONAR_rotate_left_degrees(sweep_angle_degrees)

  sonar_sweep_readings = SONAR_perform_sweep_and_get_readings(sweep_data.SWEEP_ANGLE * 2)

  SONAR_rotate_left_degrees(sweep_angle_degrees)

  DEBUG_print_sonar_readings(sonar_sweep_readings)

  return find_bottle_angle(sonar_sweep_readings)


def SONAR_find_angle_to_rotate_to_target_radians(waypoint_id):
    assert(waypoint_id == 'a' or waypoint_id == 'b' or waypoint_id == 'c')
    sweep_data = SweepData.A if waypoint_id == 'a' else (SweepData.B if waypoint_id == 'b' else SweepData.C)
    return SONAR_perform_sweep_and_get_target_angle_radians(sweep_data)

