# LEGO type:standard slot:8 autostart

from spike import PrimeHub, LightMatrix, Button, StatusLight, ForceSensor, MotionSensor, Speaker, ColorSensor, App, DistanceSensor, Motor, MotorPair
from spike.control import wait_for_seconds, Timer, wait_until
from spike.operator import *
from hub import battery
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

# Braking Values
defaultStopAction='brake'
motorPair.set_stop_action(defaultStopAction)


# Re-Usable Functions
def findColor(targetColor, colorSensor, leftMotorSpeed, rightMotorSpeed):
    # With the specified color sensor, it finds the specified color moving
    # at the specified left and right motor speeds.
    while greater_than(colorSensor.get_reflected_light(),  targetColor):
        motorPair.start_tank(leftMotorSpeed,rightMotorSpeed)
    motorPair.stop()

def startMission():
    # Resets all values for each motor and the gyro sensor.
    megaBotsPrime.light_matrix.show_image('SQUARE')
    megaBotsPrime.right_button.wait_until_pressed()
    megaBotsPrime.light_matrix.off()
    wait_for_seconds(0.2)
    leftMotor.set_degrees_counted(0)
    rightMotor.set_degrees_counted(0)
    frontMotor.set_degrees_counted(0)
    backMotor.set_degrees_counted(0)
    gyroSensor.reset_yaw_angle()

def gyroNormalize():
    if gyroSensor.get_yaw_angle() < 0:
        normalizeAngle = gyroSensor.get_yaw_angle() + 360
    else:
        normalizeAngle = gyroSensor.get_yaw_angle()
    return normalizeAngle

def m3Turn(targetGyro, offsetGyro, pauseTime, leftMotorSpeed, rightMotorSpeed):
    turn = "right" if leftMotorSpeed > rightMotorSpeed else "left"
    offsetGyro = offsetGyro if turn == "left" else offsetGyro * -1
    wait_for_seconds(pauseTime)
    motorPair.start_tank(leftMotorSpeed, rightMotorSpeed)
    wait_until(gyroNormalize, equal_to, targetGyro + offsetGyro)
    motorPair.stop()

def showBatteryLevel():
    megaBotsPrime.light_matrix.write(battery.capacity_left())

def gyroStraight(distance, motorSpeed, multiplier, referenceMotor):
    beginYaw = gyroSensor.get_yaw_angle()
    referenceMotor.set_degrees_counted(0)
    while abs(referenceMotor.get_degrees_counted()) < distance:
        yawOffset = gyroSensor.get_yaw_angle() - beginYaw
        motorPair.start_tank(int((motorSpeed - yawOffset * multiplier)), int((motorSpeed + yawOffset * multiplier)))
    motorPair.stop()

startMission()

#Go forward to approach Television
motorPair.set_stop_action('coast')
motorPair.move_tank(200, "degrees", 40, 40)
motorPair.set_stop_action(defaultStopAction)

#Slowly push Television in
motorPair.move_tank(100, "degrees", 10, 10)

#Push Television upright
motorPair.move_tank(30, "degrees", 10, 10)

#Back up
motorPair.move_tank(300, "degrees", -30, -30)

#Turn to face South East, back facing hybrid car 
m3Turn(135, 0, 0, 15, -15)

#Back up to beside Toy Factory
motorPair.move_tank(750, "degrees", -40, -40)

#Flick Rechargeable Battery
motorPair.move_tank(200, "degrees", -40, 60)

#Double wheel turn to face wind turbine, back facing toy factory
m3Turn(50, 0, 0, 10, -10)

#Back up to Toy Factory
motorPair.move_tank(180, "degrees", -15, -15)

#Release energy units
backMotor.run_for_degrees(100, -50)

#Adjust angle to face Wind Turbine
m3Turn(45, 0, 0, 0, 10)

#Go to Wind Turbine
findColor(blackThreshold, leftColor, 20, 20)

#Collect energy units from Wind Turbine
for i in range(3):
    windTurbineSpeed=25
    windTurbineDistance=80
    adjust=-20 if i==0 else 0
    adjustedWindTurbineDistance=windTurbineDistance+adjust
    motorPair.move_tank(adjustedWindTurbineDistance, "degrees", windTurbineSpeed, windTurbineSpeed)
    motorPair.set_stop_action('coast')
    adjust=150 if i==2 else 0
    adjustedWindTurbineDistance=windTurbineDistance+adjust
    motorPair.move_tank(adjustedWindTurbineDistance, "degrees", windTurbineSpeed * -1, windTurbineSpeed * -1)
    motorPair.set_stop_action(defaultStopAction)

#Turn to face Toy Factory
m3Turn(225, 0, 0, -10, 10)

#Turn so back faces blue base, leave energy units in rechargeable battery station
m3Turn(330, 0, 0, 10, -10)

SystemExit