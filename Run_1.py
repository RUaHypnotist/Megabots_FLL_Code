# LEGO type:standard slot:1 autostart

from spike import PrimeHub, ColorSensor, Motor, MotorPair
from spike.control import wait_for_seconds, Timer, wait_until
from spike.operator import *
from hub import battery
from math import *

#Initialization
megaBotsPrime = PrimeHub()

# Motor and Sensor Definitions
gyroSensor = megaBotsPrime.motion_sensor
leftMotorPort = 'A'
leftMotor = Motor(leftMotorPort)
rightMotorPort = 'E'
rightMotor = Motor(rightMotorPort)
motorPair = MotorPair(leftMotorPort, rightMotorPort)

# Positive is down for attachment 1, first run, backMotor.
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

#Turn towards hydroelectric dam, 1st turn
m3Turn(40, 0, 0, 20, 0)

#Move towards dam
motorPair.move_tank(250, "degrees", 30, 30)

# Flick the water unit
motorPair.move_tank(150, "degrees", -40, 60)

#Move forward to clear hydroelectric dam
motorPair.move_tank(20, "degrees", 20, 20)

#Turn left toward North, 2nd turn
m3Turn(0, 0, 0, 0, -25)

#Go forward until we hit the line in front of the solar farm (east/west line)
findColor(blackThreshold, rightColor, 25, 25)

#Turn East, 3rd turn
m3Turn(92, 0, 0, 20, 0)

#Go forward until hit the North/South line in front of the Smart Grid
findColor(blackThreshold, rightColor, 30, 30)

#Go forward to clear the line
motorPair.move_tank(50, "degrees", 30, 30)

#Turn South, 4th turn, back facing the Smart Grid
m3Turn(179, 0, 0, 20, 0)

#Move back towards Smart Grid
motorPair.move_tank(220 , "degrees", -20, -20)

#Drop the back hook
backMotor.run_for_degrees(140,70)

#Pull Smart Grid lever
motorPair.move_tank(60, "degrees", 20, 20)

#Slight Backup to free the hook
motorPair.move_tank(5, "degrees", -5, -5)

#Raise the back hook
backMotor.run_for_degrees(140,-50)

#Move forward to the hydrogen plant
motorPair.move_tank(180, "degrees", 30, 30)

#Turn N/NW toward Solar Farm, 5th turn
m3Turn(335, 0, 0, -15, 15)

#Go towards Solar Farm
motorPair.move_tank(260, "degrees", 30, 30)

#Slow curve turn to collect first energy unit, 6th turn
m3Turn(275, 0, 0, 13, 20)

#Turn to SouthWest, 7th turn
m3Turn(220, 0, 0, -10, 10)

#Find the black line to line up with Oil Platform lever
findColor(blackThreshold, leftColor, 20, 20)

# Move Southwest toward the Oil Platform
motorPair.move_tank(220, "degrees", 20, 20)

# Turn to Oil Platform
m3Turn(261, 0, 0, 10, -10)

# Pump the Oil Platform 3 Times
rightMotor.set_degrees_counted(0)
for i in range(3):
    oilSpeed=15
    oilDistance=80
    startAdjust=40 if i==0 else 0
    adjustedOilDistance=oilDistance+startAdjust
    motorPair.move_tank(adjustedOilDistance, "degrees", oilSpeed, oilSpeed)
    motorPair.set_stop_action('coast')
    adjust= (rightMotor.get_degrees_counted() - oilDistance - startAdjust - 30) if i==2 else 0
    adjustedOilDistance=oilDistance+adjust
    motorPair.move_tank(adjustedOilDistance, "degrees", oilSpeed * -1, oilSpeed * -1)
    motorPair.set_stop_action(defaultStopAction)

#Turn towards Red Base
m3Turn(215, 0, 0, 0, 20)

# Move to Red Base to drop of energy
motorPair.move_tank(500, "degrees", 40, 40)

# Move back towards Hydroelectric dam
motorPair.move_tank(600, "degrees", -40, -40)

# Turn behind Hydroelectric dam
m3Turn(165, 0, 0, -20, 0)

# Sweep Past Hydroelectric dam, dropping water and energy 
m3Turn(225, 0, 0, 25, 15)

#Go forward
motorPair.move_tank(150, "degrees", 30, 30)

# Turn to South
m3Turn(183, 0, 0.5, 0, 20)

# Back Up Toward Energy Storage
motorPair.move_tank(1.5 , "seconds", -50, -50)

#Make sure isn't brushing up on the Energy Storage
motorPair.move_tank(20, "degrees", 10, 10)

#Drop the back hook
backMotor.run_for_degrees(150,70)

# Start South Toward Base
motorPair.move_tank(300, "degrees", 80, 80)

# Turn SouthWest Toward Base
m3Turn(230, 0, 0, 40, 30)

# Return To Base
motorPair.move_tank(310, "degrees", 90, 90)

SystemExit