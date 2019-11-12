import time
import brickpi3
import math

BP = brickpi3.BrickPi3()

SONAR_PORT = BP.PORT_1
SONAR_INITIALISED = False

PORT_A = BP.PORT_A
PORT_B = BP.PORT_B
PORT_C = BP.PORT_C
RIGHT_WHEEL = PORT_B
LEFT_WHEEL = PORT_C

class ScalingFactors:
   movement = 1.11 * 360 / 229
   rotation = 1.09 * 360 / 229


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

def _move(scaling, mm_left, mm_right):
  # -1 factor because big wheels at the front!
  delta_encoder_left = (-1.0) * scaling * mm_left
  delta_encoder_right = (-1.0) * scaling * mm_right

  left_stop_threshold = 0.99 * (get_motor_position(LEFT_WHEEL) + delta_encoder_left)
  right_stop_threshold = 0.99 * (get_motor_position(RIGHT_WHEEL) + delta_encoder_right)

  BP.set_motor_position(LEFT_WHEEL, get_motor_position(LEFT_WHEEL) + delta_encoder_left)
  BP.set_motor_position(RIGHT_WHEEL, get_motor_position(RIGHT_WHEEL) + delta_encoder_right)

  limit = 10
  timeout = 0
  difference = -1337

  while True:
    left = abs(get_motor_position(LEFT_WHEEL))
    right = abs(get_motor_position(RIGHT_WHEEL))
    left_stop = abs(left_stop_threshold)
    right_stop = abs(right_stop_threshold)

#    if (left >= left_stop and right >= right_stop):
#      break

    if timeout == 20:
      break

    prev_difference = difference
    difference = abs(min(
      (left_stop - left) / (abs(delta_encoder_left) + 0.0001),
      (right_stop - right) / (abs(delta_encoder_right) + 0.0001)
    ))

    if difference == prev_difference:
      timeout = timeout + 1

    (_, _, _, left_dps) = BP.get_motor_status(LEFT_WHEEL)
    (_, _, _, right_dps) = BP.get_motor_status(RIGHT_WHEEL)

    right_limit_adjust = (abs(left_dps) - abs(right_dps)) / 7

    #print(right_limit_adjust)

    if difference > 0.9:
      limit = limit + 3
    elif difference < 0.1:
      limit = limit - 3

    _set_limit_at(limit, limit + right_limit_adjust)
    time.sleep(0.1)

  BP.set_motor_dps(LEFT_WHEEL, 0)
  BP.set_motor_dps(RIGHT_WHEEL, 0)

def move(mm):
  _move(ScalingFactors.movement, mm, mm)

def move_cm(cm):
  move(cm * 10)

def move_with_speed(speed):
  BP.set_motor_dps(PORT_B, speed)
  BP.set_motor_dps(PORT_C, speed)

# Idea is that for tiny turns, we have a threshold between 1 and 3 degrees
def _threshold(degrees):
  return max(1, min(3.5, 1/(math.sqrt(abs(degrees))) * 60 * math.pi))

def turn_left(degrees):
  _move(ScalingFactors.rotation, -degrees, degrees)

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
  if left_percentage < 10:
    left_percentage = 10

  if right_percentage < 10:
    right_percentage = 10

  BP.set_motor_limits(LEFT_WHEEL, left_percentage)
  BP.set_motor_limits(RIGHT_WHEEL, right_percentage)

def _set_sonar_sensor():
  BP.set_sensor_type(BP.PORT_1 + BP.PORT_2 + BP.PORT_3 + BP.PORT_4, BP.SENSOR_TYPE.NONE)
  time.sleep(0.3)
  BP.set_sensor_type(SONAR_PORT, BP.SENSOR_TYPE.NXT_ULTRASONIC)
  time.sleep(0.3)

def get_sonar_cm():
  while True:
    try:
      return BP.get_sensor(SONAR_PORT)
    except (IOError, brickpi3.SensorError):
      _set_sonar_sensor()

def get_sonar_mm():
    return get_sonar_cm() * 10

def total_reset():
    BP.reset_all()
    BP.reset_motor_encoder(PORT_B)
    BP.reset_motor_encoder(PORT_C)
    BP.reset_motor_encoder(PORT_A)
    BP.reset_motor_encoder(SONAR_PORT)

def reset_encoders():
    BP.reset_motor_encoder(PORT_B)
    BP.reset_motor_encoder(PORT_C)
