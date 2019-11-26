from math import atan2, cos, sin, degrees, radians, sqrt, hypot, pi

def angle_description(angle_rad):
    return str(degrees(angle_rad)) + "(" + str(angle_rad) + ")"


def DEBUG_print_current_state_rad(x_cm, y_cm, angle_rad):
    print()
    print()
    print("### CURRENT POSITION: (x_cm, y_cm, angle_deg, (angle_rad)) = ",
           x_cm, y_cm, angle_description(angle_rad))


def DEBUG_print_target_state_rad(target_x_cm, target_y_cm, target_angle_rad):
    print()
    print()
    print("/// TARGET POSITION")
    print("Target X and Y = ", target_x_cm, target_y_cm)
    print("Final absolute angle I need to get to = ", angle_description(target_angle_rad))


def DEBUG_print_delta_state_rad(delta_x_cm, delta_y_cm, delta_angle_rad):
    print()
    print()
    print(">>> DELTA POSITION")
    print("I need to move in y by = ", delta_y_cm)
    print("I need to move in x by = ", delta_x_cm)
    print("I need to move forward by = ", hypot(delta_x_cm, delta_y_cm))
    print("I need to rotate by = ", angle_description(delta_angle_rad))


def DEBUG_print_sonar_readings(sonar_readings):
    print()
    print()
    print("+++ SONAR SWEEP READINGS")
    print(sonar_readings)
