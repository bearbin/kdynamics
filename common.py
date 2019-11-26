import time
import math
from enum import Enum
from rendering import drawWalls, drawPath

import brickpi333 as brickpi3
BP = brickpi3.BrickPi333()

# import brickpi3
# BP = brickpi3.BrickPi3()


##### CONSTANTS #####

SONAR_PORT = BP.PORT_3
PORT_A = BP.PORT_A
PORT_B = BP.PORT_B
PORT_C = BP.PORT_C
RIGHT_WHEEL = PORT_B
LEFT_WHEEL = PORT_C
SONAR_MOTOR = PORT_A
LEFT_BUMPER = BP.PORT_4
RIGHT_BUMPER = BP.PORT_2
BUMP_CHECK_TRIES = 10
BUMP_BACKUP_DISTANCE_CM = 10
SONAR_DELTA = 4

SENSOR_RESET_SLEEP = 0.1

class BumpStatus(Enum):
  NONE = 0
  RIGHT = 1
  LEFT = 2
  BOTH = 3

class ScalingFactors:
   movement = 1.115 * 360 / 229
   rotation = 1.155 * 360 / 229


##### RESETTING #####

def total_reset():
    print("TOTAL RESET")
    BP.reset_all()
    BP.reset_motor_encoder(PORT_B)
    BP.reset_motor_encoder(PORT_C)
    BP.reset_motor_encoder(PORT_A)
    BP.reset_motor_encoder(SONAR_PORT)

def reset_encoders():
    BP.reset_motor_encoder(PORT_B)
    BP.reset_motor_encoder(PORT_C)


##### GETTERS #####

def get_motor_power(BP, port):
    return BP.get_motor_status(port)[1]

def get_motor_position(port):
  return BP.get_motor_status(port)[2]


##### INITIALIZATION #####

def _set_limit_at(left_percentage, right_percentage):
  if left_percentage < 20:
    left_percentage = 20

  if right_percentage < 20:
    right_percentage = 20

  BP.set_motor_limits(LEFT_WHEEL, left_percentage)
  BP.set_motor_limits(RIGHT_WHEEL, right_percentage)

def set_limit_at(percentage):
  _set_limit_at(percentage, percentage)

def set_sensors():
  _set_sensors()

def _sonar_reset_sleep():
  time.sleep(SENSOR_RESET_SLEEP)

def _set_sensors():
  BP.set_sensor_type(BP.PORT_1 + BP.PORT_2 + BP.PORT_3 + BP.PORT_4, BP.SENSOR_TYPE.NONE)
  _sonar_reset_sleep()

  BP.set_sensor_type(SONAR_PORT, BP.SENSOR_TYPE.NXT_ULTRASONIC)
  _sonar_reset_sleep()

  for bumper in [LEFT_BUMPER, RIGHT_BUMPER]:
    BP.set_sensor_type(bumper, BP.SENSOR_TYPE.TOUCH)
    _sonar_reset_sleep()


##### MOVEMENT #####

def _compute_percentage_yet_to_go(left_stop, left, right_stop, right, delta_encoder):
  if abs(delta_encoder) < 0.1:
    return 0
  return max(abs(right_stop - right), abs(left_stop - left)) / abs(delta_encoder)

def _move(scaling, mm, turn, delta_fun, bump_check, check_stopping_condition = lambda: False):
  # -1 factor because big wheels at the front!
  delta_encoder = (-1.0) * scaling * mm
  left_delta_encoder = -delta_encoder if turn else delta_encoder

  left_stop_threshold = get_motor_position(LEFT_WHEEL) + left_delta_encoder
  right_stop_threshold = get_motor_position(RIGHT_WHEEL) + delta_encoder

  BP.set_motor_position(LEFT_WHEEL, left_stop_threshold)
  BP.set_motor_position(RIGHT_WHEEL, right_stop_threshold)

  timeout = 0
  difference = 1
  acceleration_profile = 350
  max_power = 0.1 * acceleration_profile # Max power achieved at 10% of journey

  left_stop = abs(left_stop_threshold)
  right_stop = abs(right_stop_threshold)

  initial_left = abs(get_motor_position(LEFT_WHEEL))

  while True:
    if check_stopping_condition():
        break

    left = abs(get_motor_position(LEFT_WHEEL))
    right = abs(get_motor_position(RIGHT_WHEEL))

    if bump_check:
        bump_status = check_bump_bool()
        if bump_status:
          print('BUMP DETECTED')
          BP.set_motor_dps(LEFT_WHEEL, 0)
          BP.set_motor_dps(RIGHT_WHEEL, 0)
          bump_restore_and_rotate()
          return (left - initial_left) / scaling / 10 - BUMP_BACKUP_DISTANCE_CM

    prev_difference = difference
    difference = _compute_percentage_yet_to_go(left_stop, left, right_stop, right, delta_encoder)

#    print((timeout, delta_encoder, (abs(delta_encoder) / 5 + difference * 10)))
#    if timeout >= (abs(delta_encoder) / 5 + difference * 10):
#    print(max(abs(left_stop - left), abs(right_stop - right)))
    #if max(abs(left_stop - left), abs(right_stop - right)) < 1 or timeout == 10:
    if abs(right_stop - right) < 1.5 or timeout == 10:
      break

    delta_fun((prev_difference - difference) * mm * 0.1)

    if prev_difference == difference:
      timeout = timeout + 1

    (_, _, _, left_dps) = BP.get_motor_status(LEFT_WHEEL)
    (_, _, _, right_dps) = BP.get_motor_status(RIGHT_WHEEL)

    right_limit_adjust = max(-4, min(4, (abs(left_dps) - abs(right_dps)) / 7))

    if difference > 0.9:
      limit = (1 - difference) * acceleration_profile
    elif difference < 0.1:
      limit = (1 - difference) * -acceleration_profile + acceleration_profile
    else:
      limit = max_power

    limit = 25

    _set_limit_at(limit, limit + right_limit_adjust)
    time.sleep(0.01)

  BP.set_motor_dps(LEFT_WHEEL, 0)
  BP.set_motor_dps(RIGHT_WHEEL, 0)

def move(mm, delta_fun = lambda x: x, check_bumps = False,
         check_stopping_condition = lambda: False):
  return _move(ScalingFactors.movement, mm, False, delta_fun, check_bumps, check_stopping_condition)

def move_cm(cm, delta_fun = lambda x: x):
  move(cm * 10, delta_fun)

def move_cm_check_bumps(cm, delta_fun = lambda x: x):
  return move(cm * 10, delta_fun, True)

def move_cm_check_bumps_and_condition(cm, check_stopping_condition, delta_fun = lambda x: x):
  move(cm * 10, delta_fun, True, check_stopping_condition)

def move_with_speed(speed):
  BP.set_motor_dps(PORT_B, speed)
  BP.set_motor_dps(PORT_C, speed)


##### TURNING #####

# Idea is that for tiny turns, we have a threshold between 1 and 3 degrees
def _threshold(degrees):
  return max(1, min(3.5, 1/(math.sqrt(abs(degrees))) * 60 * math.pi))

def turn_left(degrees, delta_fun = lambda x: x):
  _move(ScalingFactors.rotation, degrees, True, delta_fun, False)

def _turn_left(degrees):
  if degrees == 0:
    return

  # -1 factor because big wheels at the front!
  print("Flesh bag detected at ", degrees, " degrees - proceeding to exterminate")
  delta_encoder = (-1.0) * ScalingFactors.rotation * degrees

  final_left =  (get_motor_position(LEFT_WHEEL) - delta_encoder)
  final_right  =  (get_motor_position(RIGHT_WHEEL) + delta_encoder)

  stop_threshold = threshold(degrees)
  print(stop_threshold)

  BP.set_motor_position(LEFT_WHEEL, final_left)
  BP.set_motor_position(RIGHT_WHEEL, final_right)

  while (abs(get_motor_position(LEFT_WHEEL) - final_left) > stop_threshold and
         abs(get_motor_position(RIGHT_WHEEL) - final_right) > stop_threshold):
    #print(abs(get_motor_position(RIGHT_WHEEL) - final_right))
    #print(abs(get_motor_position(RIGHT_WHEEL) - final_right))
    continue
  print("Turn complete")


def turn_left_radians(angle_radians):
    turn_left(math.degrees(angle_radians))


##### SONAR #####

def get_sonar_cm():
  while True:
    try:
      measurements = [BP.get_sensor(SONAR_PORT) + SONAR_DELTA for i in range(5)]
      measurements.sort()
      return measurements[2] # Return the median distance
    except (IOError, brickpi3.SensorError):
      print("Got an error while reading sonar")
      _set_sensors()

def get_sonar_mm():
    return get_sonar_cm() * 10

def turn_sonar_left(degrees):
  curr_angle = get_motor_position(SONAR_MOTOR)
  BP.set_motor_position(SONAR_MOTOR, curr_angle + degrees)


##### BUMPING #####

def check_bump():
    for i in range(BUMP_CHECK_TRIES):
        try:
            value_left = BP.get_sensor(LEFT_BUMPER)
            value_right = BP.get_sensor(RIGHT_BUMPER)

        # print('bump readings (l/r):')
        #    print(value_left)
        #    print(value_right)

            if value_left:
                return BumpStatus.BOTH if value_right else BumpStatus.LEFT
            if value_right:
                return BumpStatus.BOTH if value_left else BumpStatus.RIGHT
            return BumpStatus.NONE
        except (IOError, brickpi3.SensorError):
            _set_sensors()
            print("Error while checking bump")
    return BumpStatus.NONE

def check_bump_bool():
  return check_bump() != BumpStatus.NONE

def bump_restore_and_rotate():
    move_cm(-BUMP_BACKUP_DISTANCE_CM)
    turn_left(180)
    print("FINISHED BUMP RESTORE")


##### MISC #####

def normalise_rads(angle):
  return math.atan2(math.sin(angle), math.cos(angle))


ORIGINAL_WAYPOINTS = [
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


# Metres
scan_waypoint_a = (0.90, 0.30)
scan_waypoint_b = (0.90, 0.70)
scan_waypoint_c = (0.42, 0.30)
