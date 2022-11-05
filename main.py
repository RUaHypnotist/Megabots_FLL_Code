# LEGO type:standard slot:10 autostart

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
    #startingAngle = gyroNormalize()
    #finalAngle = targetGyro
    wait_for_seconds(pauseTime)
    motorPair.start_tank(leftMotorSpeed, rightMotorSpeed)
    wait_until(gyroNormalize, equal_to, targetGyro)
    motorPair.stop()


def showBatteryLevel():
    megaBotsPrime.light_matrix.write(battery.capacity_left())

startMission()

#Turn towards hydroelectric dam, 1st turn
m3Turn(40, 0, 0, 20, 0)

#Move towards dam
motorPair.move_tank(250, "degrees", 30, 30)

#whip the water unit
m3Turn(335, 0, 0, -40, 60)

#Turn left toward North, 2nd turn

m3Turn(2, 0, 0, 0, -25)

findColor(blackThreshold, rightColor, 20, 20)

#Turn East, 3rd turn
m3Turn(90, 0, 0, 20, 0)

findColor(blackThreshold, rightColor, 20, 20)

motorPair.move_tank(50, "degrees", 30, 30)

#Turn South, 4th turn
m3Turn(179, 0, 0, 20, 0)

#Move back towards Smart Grid
motorPair.move_tank(200, "degrees", -20, -20)

#Drop the back hook
backMotor.run_for_degrees(140,70)

#Pull Smart Grid lever
motorPair.move_tank(100, "degrees", 10, 10)

#Raise the back hook
backMotor.run_for_degrees(140,-50)

#Move forward to the hydrogen plant
motorPair.move_tank(170, "degrees", 20, 20)

#Turn N/NW toward Solar Farm, 5th turn
m3Turn(335, 0, 0, -10, 10)

#Go towards Solar Farm
motorPair.move_tank(270, "degrees", 30, 30)

#Slow curve turn to collect first energy unit, 6th turn
m3Turn(275, 0, 0, 13, 20)

#Turn to SouthWest, 7th turn
m3Turn(220, 0, 0, -10, 10)

#Find the black line to line up with oil rig lever
findColor(blackThreshold, rightColor, 20, 20)

# Move Southwest toward the Oil Rig
motorPair.move_tank(160, "degrees", 20, 20)

# Turn to Oil Rig
m3Turn(263, 0, 0, 10, -10)

# Pump the Oil Station 3 Times
for i in range(3):
    oilRigSpeed=15
    oilRigDistance=80
    adjust=20 if i==0 else 0
    adjustedOilRigDistance=oilRigDistance+adjust
#    print("Run A ", str(i), " adjustDistance ", adjustedOilRigDistance)
    motorPair.move_tank(adjustedOilRigDistance, "degrees", oilRigSpeed, oilRigSpeed)
    motorPair.set_stop_action('coast')
    adjust=-10 if i==2 else 0
    adjustedOilRigDistance=oilRigDistance+adjust
#    print("Run B ", str(i), " adjustDistance ", adjustedOilRigDistance)
    motorPair.move_tank(adjustedOilRigDistance, "degrees", oilRigSpeed * -1, oilRigSpeed * -1)
    motorPair.set_stop_action(defaultStopAction)

#Turn towards Red Base
m3Turn(215, 0, 0, 0, 20)

# Move to Red Base to drop of energy
motorPair.move_tank(500, "degrees", 40, 40)

# Move back towards Hydro Plant
motorPair.move_tank(600, "degrees", -40, -40)

# Turn behind Hydro Plant
m3Turn(172, 0, 0, -20, 0)

# Sweep Past Hydro Plant, dropping water and energy
m3Turn(225, 0, 0, 20, 15)

# Turn to South
m3Turn(182, 0, 0.5, 0, 20)

# Back Up Toward Energy Storage
motorPair.move_tank(600, "degrees", -40, -40)

#Make sure isn't brushing up on the Energy Storage
motorPair.move_tank(20, "degrees", 10, 10)

#Drop the back hook
backMotor.run_for_degrees(150,70)

# Start South Toward Base
motorPair.move_tank(300, "degrees", 70, 70)

# Turn SouthWest Toward Base
m3Turn(220, 0, 0, 40, 30)

# Return To Base
motorPair.move_tank(310, "degrees", 70, 70)

showBatteryLevel()