import time
# import brickpi333 as brickpi3
import brickpi3
import math
from enum import Enum

# BP = brickpi3.BrickPi333()
BP = brickpi3.BrickPi3()

SONAR_PORT = BP.PORT_3
SONAR_INITIALISED = False

PORT_A = BP.PORT_A
PORT_B = BP.PORT_B
PORT_C = BP.PORT_C
RIGHT_WHEEL = PORT_B
LEFT_WHEEL = PORT_C
SONAR_MOTOR = PORT_A
LEFT_BUMPER = BP.PORT_3
RIGHT_BUMPER = BP.PORT_2


class ScalingFactors:
   movement = 1.115 * 360 / 229
   rotation = 1.155 * 360 / 229


# LIMIT 25
  # rotation = 1.13 * 360 / 229
  # almost perfect
  # almost perfect

  # rotation = 1.15 * 360 / 229
  # overrotation a bit (2cm)   
  # overrotation a bit (2cm)   
  # overrotation a bit (1cm)   

def get_motor_power(BP, port):
    return BP.get_motor_status(port)[1]

def get_motor_position(port):
  return BP.get_motor_status(port)[2]

def _compute_percentage_yet_to_go(left_stop, left, right_stop, right, delta_encoder):
  if abs(delta_encoder) < 0.1:
    return 0

  return max(abs(right_stop - right), abs(left_stop - left)) / abs(delta_encoder)

def _move(scaling, mm, turn, delta_fun):
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

  while True:
    left = abs(get_motor_position(LEFT_WHEEL))
    right = abs(get_motor_position(RIGHT_WHEEL))

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
    #print(limit)
    #print(difference)

    _set_limit_at(limit, limit + right_limit_adjust)
    time.sleep(0.01)

  BP.set_motor_dps(LEFT_WHEEL, 0)
  BP.set_motor_dps(RIGHT_WHEEL, 0)

def move(mm, delta_fun = lambda x: x):
  _move(ScalingFactors.movement, mm, False, delta_fun)

def move_cm(cm, delta_fun = lambda x: x):
  move(cm * 10, delta_fun)

def move_with_speed(speed):
  BP.set_motor_dps(PORT_B, speed)
  BP.set_motor_dps(PORT_C, speed)

# Idea is that for tiny turns, we have a threshold between 1 and 3 degrees
def _threshold(degrees):
  return max(1, min(3.5, 1/(math.sqrt(abs(degrees))) * 60 * math.pi))

def turn_left(degrees, delta_fun = lambda x: x):
  _move(ScalingFactors.rotation, degrees, True, delta_fun)

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

def _set_limit_at(left_percentage, right_percentage):
  if left_percentage < 20:
    left_percentage = 20

  if right_percentage < 20:
    right_percentage = 20

  BP.set_motor_limits(LEFT_WHEEL, left_percentage)
  BP.set_motor_limits(RIGHT_WHEEL, right_percentage)

def turn_sonar_left(degrees):
  curr_angle = get_motor_position(SONAR_MOTOR)
  BP.set_motor_position(SONAR_MOTOR, curr_angle + degrees)

def _set_sensors():
  BP.set_sensor_type(BP.PORT_1 + BP.PORT_2 + BP.PORT_3 + BP.PORT_4, BP.SENSOR_TYPE.NONE)
  time.sleep(0.3)

  BP.set_sensor_type(SONAR_PORT, BP.SENSOR_TYPE.NXT_ULTRASONIC)
  time.sleep(0.3)

  for bumper in [LEFT_BUMPER, RIGHT_BUMPER]:
    BP.set_sensor_type(bumper, BP.SENSOR_TYPE.TOUCH)
    time.sleep(0.3)


def get_sonar_cm():
  while True:
    try:
      measurements = [BP.get_sensor(SONAR_PORT) + 4 for i in range(5)]
      measurements.sort()
      return measurements[2] # Return the median distance
    except (IOError, brickpi3.SensorError):
      print("Got an error while reading sonar")
      _set_sensors()

def get_sonar_mm():
    return get_sonar_cm() * 10

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

BUMP_CHECK_TRIES = 10

class BumpStatus(Enum):
  NONE = 0
  RIGHT = 1
  LEFT = 2
  BOTH = 3

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

BUMP_BACKUP_DISTANCE_CM = 10

def bump_restore_and_rotate():
    move_cm(-BUMP_BACKUP_DISTANCE_CM)
    turn_left(180)

# BP.set_sensor_type(BP.PORT_1, BP.SENSOR_TYPE.TOUCH)
# 
# try:
#     while True:
#         # read and display the sensor value
#         # BP.get_sensor retrieves a sensor value.
#         # BP.PORT_1 specifies that we are looking for the value of sensor port 1.
#         # BP.get_sensor returns the sensor value (what we want to display).
#         try:
#             value = BP.get_sensor(BP.PORT_1)
#             print(value)
#         except brickpi3.SensorError as error:
#             print(error)
#         
#         time.sleep(0.02)  # delay for 0.02 seconds (20ms) to reduce the Raspberry Pi CPU load.
# 
# except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
#     BP.reset_all()        # Unconfigure the sensors, disable the motors, and restore the LED to the control of the BrickPi3 firmware.
