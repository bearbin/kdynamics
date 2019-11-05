import time
import sys
import brickpi3
from rendering import *

BP = brickpi3.BrickPi3()

SONAR_PORT = BP.PORT_1
SONAR_INITIALISED = False
PORT_A = BP.PORT_A
PORT_B = BP.PORT_B
PORT_C = BP.PORT_C
RIGHT_WHEEL = PORT_B
LEFT_WHEEL = PORT_C

class ScalingFactors:
   movement = 1.0 * 360 / 229
   rotation = 1.13 * 360 / 229


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

def move(mm):
  # -1 factor because big wheels at the front!
  print("distance = ", mm)
  delta_encoder = (-1.0) * ScalingFactors.movement * mm
  left_stop_threshold = 0.99 * (delta_encoder + get_motor_position(PORT_B))
  right_stop_threshold = 0.99 * (delta_encoder + get_motor_position(PORT_C))

  BP.set_motor_position(PORT_B, delta_encoder + get_motor_position(PORT_B))
  BP.set_motor_position(PORT_C, delta_encoder + get_motor_position(PORT_C))

  while (abs(get_motor_position(PORT_B)) < abs(right_stop_threshold) and
    abs(get_motor_position(PORT_C)) < abs(left_stop_threshold)):
    continue
  print("Move finished")

def move_with_speed(speed):
  BP.set_motor_dps(PORT_B, speed)
  BP.set_motor_dps(PORT_C, speed)

def turn_left(degrees):
  print("Flesh bag detected at ", degrees, " degrees")
  final_encoder_pos = ScalingFactors.rotation * degrees
  stop_threshold = 0.99 * final_encoder_pos

  BP.set_motor_position(PORT_B, -final_encoder_pos + get_motor_position(PORT_B))
  BP.set_motor_position(PORT_C, final_encoder_pos + get_motor_position(PORT_C))
  while (abs(get_motor_position(PORT_B)) > abs(stop_threshold) and
    abs(get_motor_position(PORT_C)) < abs(stop_threshold)):
    continue

def set_limit_at(percentage):
  BP.set_motor_limits(PORT_B, percentage)
  BP.set_motor_limits(PORT_C, percentage)

def set_sonar_sensor():
  global SONAR_INITIALISED
  BP.set_sensor_type(BP.PORT_1 + BP.PORT_2 + BP.PORT_3 + BP.PORT_4, BP.SENSOR_TYPE.NXT_ULTRASONIC)
  BP.set_sensor_type(SONAR_PORT, BP.SENSOR_TYPE.NXT_ULTRASONIC)
  SONAR_INITIALISED = True

def get_sonar_cm():
  if not SONAR_INITIALISED:
    set_sonar_sensor()
    time.sleep(0.02)
  try:
    return BP.get_sensor(SONAR_PORT)
  except brickpi3.SensorError as e:
    print(e)
    return -1

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
