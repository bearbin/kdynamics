import time
import sys
import brickpi3
import math
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

def move(mm):
  # -1 factor because big wheels at the front!
  print("distance = ", mm)
  delta_encoder = (-1.0) * ScalingFactors.movement * mm
  left_stop_threshold = 0.99 * (get_motor_position(LEFT_WHEEL) + delta_encoder)
  right_stop_threshold = 0.99 * (get_motor_position(RIGHT_WHEEL) + delta_encoder)

  BP.set_motor_position(LEFT_WHEEL, get_motor_position(LEFT_WHEEL) + delta_encoder)
  BP.set_motor_position(RIGHT_WHEEL, get_motor_position(RIGHT_WHEEL) + delta_encoder)

  while (abs(get_motor_position(LEFT_WHEEL)) < abs(left_stop_threshold) and
    abs(get_motor_position(RIGHT_WHEEL)) < abs(right_stop_threshold)):
    continue
  print("Move finished")

def move_cm(cm):
  move(cm * 10)

def move_with_speed(speed):
  BP.set_motor_dps(PORT_B, speed)
  BP.set_motor_dps(PORT_C, speed)

# Idea is that for tiny turns, we have a threshold between 1 and 3 degrees
def threshold(degrees):
  return max(1, min(3.5, 1/(math.sqrt(abs(degrees))) * 60 * math.pi))

def turn_left(degrees):
  
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
