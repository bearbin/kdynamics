#!/usr/bin/env python3

import time
from common import *
from waypoint import *
from mcl import get_expected_signature
from math import radians
from debug import *

SONAR_ROTATION_WAIT = 0.6
SONAR_ROTATION_WAIT_SMALL = 0.1
SWEEP_STEP_DEGREES = 5

class SweepData:
    class A:
        SWEEP_ANGLE = 45
    class B:
        SWEEP_ANGLE = 45
    class C:
        SWEEP_ANGLE = 45


########################## FUNCTIONS ############################

def measure_sonar():
    reading = get_sonar_cm()
    print("Sonar reading was " + str(reading))
    time.sleep(0.02)
    return reading


def correct_sonar_turn(turn):
    return turn * 11 / 7.5


BP.set_motor_limits(PORT_A, 25)


def SONAR_rotate_left_degrees(angle_degrees):
    turn_sonar_left(correct_sonar_turn(angle_degrees))
    wait_time = SONAR_ROTATION_WAIT if angle_degrees > 10 else SONAR_ROTATION_WAIT_SMALL
    time.sleep(wait_time)


def SONAR_record_into(readings):
    reading = measure_sonar()
    readings.append(reading)


def compute_sweep_steps_num(sweep_angle_degrees, sweep_step_degrees):
    return int(sweep_angle_degrees / sweep_step_degrees)


def SONAR_perform_sweep_and_get_readings(sweep_angle_degrees):
    sweep_steps_num = compute_sweep_steps_num(sweep_angle_degrees, SWEEP_STEP_DEGREES)
    readings = []

    for angle_degrees in range(sweep_steps_num):
        SONAR_record_into(readings)
        SONAR_rotate_left_degrees(-SWEEP_STEP_DEGREES)
    SONAR_record_into(readings)

    return readings


def compute_estimated_ideal_sonar_readings(sweep_data):
    pos = get_robot_position()
    sweep_angle = sweep_data.SWEEP_ANGLE
    return get_expected_signature(pos[0], pos[1], pos[2], -sweep_angle, sweep_angle, SWEEP_STEP_DEGREES)


def find_bottle_angle(actual_sonar_readings, sweep_data):
    estimated_ideal_sonar_readings = compute_estimated_ideal_sonar_readings(sweep_data)

    print(estimated_ideal_sonar_readings)

    # TODO: Diff algorithm
    return 0


def SONAR_perform_sweep_and_get_target_angle_radians(sweep_data):
  sweep_angle_degrees = sweep_data.SWEEP_ANGLE

  SONAR_rotate_left_degrees(sweep_angle_degrees)
  sonar_sweep_readings = SONAR_perform_sweep_and_get_readings(sweep_data.SWEEP_ANGLE * 2)
  SONAR_rotate_left_degrees(sweep_angle_degrees)

  DEBUG_print_sonar_readings(sonar_sweep_readings)

  return find_bottle_angle(sonar_sweep_readings, sweep_data)


def SONAR_find_angle_to_rotate_to_target_radians(waypoint_id):
    assert(waypoint_id == 'a' or waypoint_id == 'b' or waypoint_id == 'c')
    sweep_data = SweepData.A if waypoint_id == 'a' else (SweepData.B if waypoint_id == 'b' else SweepData.C)
    return SONAR_perform_sweep_and_get_target_angle_radians(sweep_data)
