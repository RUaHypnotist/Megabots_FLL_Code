# LEGO type:standard slot:4 autostart

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

startMission()

while less_than(gyroSensor.get_yaw_angle(), 40):
    motorPair.start_tank(20,0)
motorPair.stop()

motorPair.move_tank(250, "degrees", 30, 30)

while greater_than(gyroSensor.get_yaw_angle(), 5):
    motorPair.start_tank(0,20)
motorPair.stop()

findColor(blackThreshold, rightColor, 20, 20)

while less_than(gyroSensor.get_yaw_angle(), 85):
    motorPair.start_tank(20,0)
motorPair.stop()

findColor(blackThreshold, rightColor, 20, 20)

motorPair.move_tank(50, "degrees", 30, 30)

while less_than(gyroSensor.get_yaw_angle(), 175):
    motorPair.start_tank(20,0)
motorPair.stop()

motorPair.move_tank(120, "degrees", -20, -20)

backMotor.run_for_degrees(175,50)

motorPair.move_tank(200, "degrees", 10, 10)

while greater_than(gyroSensor.get_yaw_angle(), -25):
    motorPair.start_tank(-10,10)
motorPair.stop()

motorPair.move_tank(200, "degrees", 30, 30)

while greater_than(gyroSensor.get_yaw_angle(), -90):
    motorPair.start_tank(-10,10)
motorPair.stop()

motorPair.move_tank(200, "degrees", 30, 30)

while greater_than(gyroSensor.get_yaw_angle(), -135):
    motorPair.start_tank(-10,10)
motorPair.stop()

# motorPair.move_tank(100, "degrees", -30, -30)

# motorPair.move_tan, "degrees", 15, 15)

# backMotor.run_for_degrees(100,-50)