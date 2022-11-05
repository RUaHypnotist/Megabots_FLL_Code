# LEGO type:standard slot:2 autostart

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
    megaBotsPrime.right_button.wait_until_pressed()
    wait_for_seconds(0.5)
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
    wait_until(gyroNormalize, equal_to, (targetGyro + offsetGyro))
    motorPair.stop()

def showBatteryLevel():
    megaBotsPrime.light_matrix.write(battery.capacity_left())

# def gyroStraight(distance, motorSpeed, multiplier, referenceMotor):
#     currentYaw = gyroSensor.get_yaw_angle()
#     referenceMotor.set_degrees_counted(0)
#     while referenceMotor.get_degrees_counted() < distance:
#         yawOffset = gyroSensor.get_yaw_angle() - currentYaw
#         print("Gyro Yaw: " , gyroSensor.get_yaw_angle())
#         print("Offset: " , yawOffset)
#         print("distance: ",referenceMotor.get_degrees_counted())
#         # steering = int(yawOffset * multiplier)
#         # motorPair.start(steering, motorSpeed)
#         motorPair.start_tank(int((motorSpeed - yawOffset * multiplier)), int((motorSpeed + yawOffset * multiplier)))
#     motorPair.stop()

# def lineFollow(distance, motorSpeed, multiplier, targetReflectedLight, referenceMotor, referenceColorSensor):
#     referenceMotor.set_degrees_counted(0)
#     while referenceMotor.get_degrees_counted() < distance:
#         print("distance: ", referenceMotor.get_degrees_counted())
#         colorOffset = int((targetReflectedLight - referenceColorSensor.get_reflected_light())*multiplier)
#         print("colorOffset: ", colorOffset)
#         motorPair.start_tank((motorSpeed - colorOffset), (motorSpeed + colorOffset))
#     motorPair.stop()

startMission()

#Leave base until right color sensor hits black line
findColor(blackThreshold, rightColor, 30, 30)

#Turn to Northeast to avoid oil platform
m3Turn(20, 0, 0, 30, 0)

#Travel Northeast until left color sensor finds black
findColor(blackThreshold, leftColor, 30, 30)

#Face North and energy storage
m3Turn(0, 10, 0, 0, 20)

#Go forward, against energy storage
motorPair.move_tank(300, "degrees", 20, 20)


#Release energy units
frontMotor.run_for_degrees(100, 50)



# lineFollow(600,10,0.2,70,rightMotor,leftColor)

#gyroStraight(1000, 30, 1.4, rightMotor)


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

sys.exit()