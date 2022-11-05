# LEGO type:standard slot:2 autostart

from spike import PrimeHub, LightMatrix, Button, StatusLight, ForceSensor, MotionSensor, Speaker, ColorSensor, App, DistanceSensor, Motor, MotorPair
from spike.control import wait_for_seconds, Timer
from spike.operator import *
from math import *

#Initialization
megaBotsPrime = PrimeHub()

# Positive is down for attachment 1, first run, backMotor.
# Motor and Sensor Definitions
gyroSensor = megaBotsPrime.motion_sensor
leftMotorPort = 'A'
leftMotor = Motor(leftMotorPort)
rightMotorPort = 'E'
rightMotor = Motor(rightMotorPort)
motorPair = MotorPair(leftMotorPort, rightMotorPort)

frontMotorPort = 'D'
frontMotor = Motor(frontMotorPort)
backMotorPort = 'C'
backMotor = Motor(backMotorPort)
leftColorPort = 'B'
leftColor = ColorSensor(leftColorPort)
rightColorPort= 'F'
rightColor = ColorSensor(rightColorPort)

#Color value variables
blackColor = 36
whiteColor = 99
colorThreshold = 3
blackThreshold = blackColor + colorThreshold
whiteThreshold = whiteColor - colorThreshold

# Re-Usable Functions
def findColor(targetColor, colorSensor, leftMotorSpeed, rightMotorSpeed):
    # With the specified color sensor, it finds the specified color moving
    # at the specified left and right motor speeds.
    while greater_than(colorSensor.get_reflected_light(),  targetColor):
        motorPair.start_tank(leftMotorSpeed,rightMotorSpeed)
    motorPair.stop()

def startMission():
    # Resets all values for each motor and the gyro sensor.
    megaBotsPrime.right_button.wait_until_pressed()
    wait_for_seconds(2)
    leftMotor.set_degrees_counted(0)
    rightMotor.set_degrees_counted(0)
    frontMotor.set_degrees_counted(0)
    backMotor.set_degrees_counted(0)
    gyroSensor.reset_yaw_angle()

# startMission()

# print('LeftMotor: ',leftMotor.get_degrees_counted())
# print('RightMotor: ',rightMotor.get_degrees_counted())
# print('FrontMotor: ',frontMotor.get_degrees_counted())
# print('BackMotor: ',backMotor.get_degrees_counted())
# print('Yaw: ', gyroSensor.get_yaw_angle())

# wait_for_seconds(5)

# print('LeftMotor: ',leftMotor.get_degrees_counted())
# print('RightMotor: ',rightMotor.get_degrees_counted())
# print('FrontMotor: ',frontMotor.get_degrees_counted())
# print('BackMotor: ',backMotor.get_degrees_counted())
# print('Yaw: ', gyroSensor.get_yaw_angle())

# backMotor.set_degrees_counted(0)
# backMotorBefore = backMotor.get_degrees_counted()
# backMotor.run_for_degrees(180)
# backMotorAfter = backMotor.get_degrees_counted()
# motorPair.move(100, "degrees", 0, 10)

# print("Before: ",backMotorBefore)
# print("After: ",backMotorAfter)
# print("Difference: ", backMotorBefore - backMotorAfter)

# findColor(blackThreshold, rightColor, 20, 20)
# findColor(blackThreshold, leftColor, 20, -20)

# print("Color Reflected: " , rightColor.get_rgb_intensity())
# while rightColor.get_reflected_light() < whiteThreshold:
#     motorPair.start(0,20)
# motorPair.stop()



#M2 Oil Truck pull to base
#motorPair.move(100, "degrees", 0, 10)
#motorPair.move(400, "degrees", 0, 30)
#backMotor.run_for_degrees(180, 50)

#while True:
#    megaBotsPrime.light_matrix.write(rightColor.get_rgb_intensity())

