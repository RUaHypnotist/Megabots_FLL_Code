# LEGO type:standard slot:8 autostart

from spike import PrimeHub, ColorSensor, Motor, MotorPair
from spike.control import wait_for_seconds, Timer, wait_until
from spike.operator import *
from math import *
import utime

#Initialization
megaBotsPrime = PrimeHub()

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
    wait_until(gyroNormalize, equal_to, targetGyro + offsetGyro)
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

#Go forward to approach Television
motorPair.set_stop_action('coast')
motorPair.move_tank(200, "degrees", 40, 40)
motorPair.set_stop_action(defaultStopAction)

#Slowly push Television in
fleep(1100, 14, 14)

#Back up
motorPair.move_tank(300, "degrees", -30, -30)

#Turn to face South East, back facing hybrid car 
m3Turn(135, 0, 0, 15, -15)

#Back up to beside Toy Factory
motorPair.move_tank(750, "degrees", -45, -45)

#Flick Rechargeable Battery
motorPair.move_tank(200, "degrees", -60, 90)

#Double wheel turn to face wind turbine, back facing toy factory
m3Turn(50, 0, 0, 15, -15)

#Back up to Toy Factory
fleep(1400, -15, -15)

#Release energy units
backMotor.run_for_degrees(100, -50)

#Adjust angle to face Wind Turbine
m3Turn(45 , 0, 0, 0, 12)

#Go to Wind Turbine
fleep(1800, 20, 20)

#Collect energy units from Wind Turbine
for i in range(3):
    windTurbineSpeed=25
    windTurbineDistance=80
    adjust=-30 if i==0 else 0
    adjustedWindTurbineDistance=windTurbineDistance+adjust
    motorPair.move_tank(adjustedWindTurbineDistance, "degrees", windTurbineSpeed, windTurbineSpeed)
    motorPair.set_stop_action('coast')
    adjust=140 if i==2 else 0
    adjustedWindTurbineDistance=windTurbineDistance+adjust
    motorPair.move_tank(adjustedWindTurbineDistance, "degrees", windTurbineSpeed * -1, windTurbineSpeed * -1)
    motorPair.set_stop_action(defaultStopAction)

#Turn to face Toy Factory
m3Turn(225, 0, 0, -12, 12)

#Turn so back faces blue base, leave energy units in rechargeable battery station
m3Turn(330, 0, 0, 20, -20)

#Go back to blue base
motorPair.move_tank(1100, "degrees", -90, -80)

startMission()

gyroStraight(2360, 90, 1.3, rightMotor)

SystemExit