# LEGO type:standard slot:2 autostart

from spike import PrimeHub, ColorSensor, Motor, MotorPair
from spike.control import wait_for_seconds, Timer, wait_until
from spike.operator import *
from math import *
import utime

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
    utime.sleep_ms(200)
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
    utime.sleep_ms(pauseTime)
    motorPair.start_tank(leftMotorSpeed, rightMotorSpeed)
    wait_until(gyroNormalize, equal_to, (targetGyro + offsetGyro))
    motorPair.stop()

def gyroStraight(distance, motorSpeed, multiplier, referenceMotor):
    beginYaw = gyroSensor.get_yaw_angle()
    referenceMotor.set_degrees_counted(0)
    while abs(referenceMotor.get_degrees_counted()) < distance:
        yawOffset = gyroSensor.get_yaw_angle() - beginYaw
        motorPair.start_tank(int((motorSpeed - yawOffset * multiplier)), int((motorSpeed + yawOffset * multiplier)))
    motorPair.stop()

# Moves each motor for a certain amount of miliseconds, and beeps when going backwards.
def fleep(time_ms, leftMotorSpeed, rightMotorSpeed):
    start = utime.ticks_ms()
    motorPair.start_tank(leftMotorSpeed, rightMotorSpeed)
    while utime.ticks_diff(utime.ticks_ms(), start) < time_ms:
        if leftMotorSpeed <= 0 and rightMotorSpeed <= 0 and time_ms >= 999:
            megaBotsPrime.speaker.beep(80, 0.7)
        utime.sleep_ms(300)
    motorPair.stop()

startMission()

#Leave base until right color sensor hits black line
findColor(blackThreshold, rightColor, 30, 30)

#Turn to Northeast to avoid oil platform
m3Turn(20, 0, 0, 20, 0)

#Travel Northeast until left color sensor finds black
findColor(blackThreshold, leftColor, 30, 30)

#Face North and energy storage
m3Turn(4, 0, 0, 0, 15)

#Go forward, against energy storage
motorPair.move_tank(1.5, "seconds", 30, 30)

#Release energy units
frontMotor.run_for_degrees(100, 50)

#Back up from energy storage until right color sensor hits black line
findColor(blackThreshold, rightColor, -30, -30)

#Back up from black line to avoid hitting the oil platform while turning
motorPair.move_tank(200, "degrees", -30, -30)

#Turn Northeast
m3Turn(45, 0, 0, 25, 0)

#Find the next black line
findColor(blackThreshold, leftColor, 30, 30)

#Turn east
m3Turn(84, 0, 0, 20, 0)

#Move parallel to water
motorPair.move_tank(200, "degrees", 20, 22)

#Release water units
backMotor.run_for_seconds(1.8 , -95 )

#Go forward until right color sensor hits the black line 
findColor(blackThreshold, rightColor, 35, 35)

#Move past line
motorPair.move_tank(200, "degrees", 25, 25)

#Turn so back faces the power plant
m3Turn(0, 0, 0, -15, 0)

#Back up to power plant
gyroStraight(500, -40, 1.5, leftMotor)

#Correct approach to power plant
#Adjust for tilted right
if gyroSensor.get_yaw_angle() > 2:
    m3Turn(359, 0, 0, 0, 5)
    rightMotor.set_degrees_counted(0)
    motorPair.move_tank(1.6 , "seconds", -15, -15)

#Adjust for tilt left
elif gyroSensor.get_yaw_angle() < -2:
    m3Turn(357, 0, 0, 3, 0)
    rightMotor.set_degrees_counted(0)
    motorPair.move_tank(1.6, "seconds", -11, -15)

#Adjust for slight tilt left
elif gyroSensor.get_yaw_angle() < 0:
    rightMotor.set_degrees_counted(0)
    motorPair.move_tank(1.6, "seconds", -13, -15)

#Adjust for extreme tilt left
elif gyroSensor.get_yaw_angle() < -4:
    rightMotor.set_degrees_counted(0)
    motorPair.move_tank(1.6, "seconds", -11, -15)

#No adjust if perfect
else:
    rightMotor.set_degrees_counted(0)
    motorPair.move_tank(1.6, "seconds", -15, -15)

#Using distance traveled, create variable for adjust
hydrogenReturnDistance = 60 + abs(rightMotor.get_degrees_counted())

#Turn to clear power plant
m3Turn(340, 0, 0, 0, 10)

# Go foward to hydrogen plant using adjusted variable
motorPair.move_tank(hydrogenReturnDistance, "degrees", 33, 30)

#Quick turn to drop off innovation module
motorPair.move_tank(60, "degrees", 75, -75)

#Turn to blue base
m3Turn(110, 0, 0, 10, -10)

#Go back to blue base
motorPair.move_tank(1300, "degrees", 70, 74)

SystemExit