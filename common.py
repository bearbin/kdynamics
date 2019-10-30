import time
import sys
import brickpi3

BP = brickpi3.BrickPi3()

SONAR_PORT = BP.PORT_1
PORT_A = BP.PORT_A
PORT_B = BP.PORT_B
PORT_C = BP.PORT_C

class ScalingFactors:
   movement = 1.075 * 360 / 229 
   rotation = 1.075 * 360 / 229

def get_motor_power(BP, port):
    return BP.get_motor_status(port)[1]

def get_motor_position(port):
  return BP.get_motor_status(port)[2]

def move(mm):
  # -1 factor because big wheels at the front!
  final_encoder_pos = (-1) * ScalingFactors.movement * mm
  stop_threshold = 0.99 * final_encoder_pos

  BP.set_motor_position(PORT_B, final_encoder_pos)
  BP.set_motor_position(PORT_C, final_encoder_pos)

  while (abs(get_motor_position(PORT_B)) < abs(stop_threshold) and
    abs(get_motor_position(PORT_C)) < abs(stop_threshold)):
    continue

def move_with_speed(speed):
  BP.set_motor_dps(PORT_B, speed)
  BP.set_motor_dps(PORT_C, speed)

def turn_left(degrees):
  final_encoder_pos = ScalingFactors.rotation * degrees
  stop_threshold = 0.99 * final_encoder_pos
  
  BP.set_motor_position(PORT_B, -final_encoder_pos)
  BP.set_motor_position(PORT_C, final_encoder_pos)


  while (abs(get_motor_position(PORT_B)) < abs(stop_threshold) and
    abs(get_motor_position(PORT_C)) > abs(stop_threshold)):
    continue

def set_limit_at(percentage):
  BP.set_motor_limits(PORT_B, percentage)
  BP.set_motor_limits(PORT_C, percentage)


def get_sonar_cm():
  try:
    return BP.get_sensor(SONAR_PORT)
  except brickpi3.SensorError:
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
