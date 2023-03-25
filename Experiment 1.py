# LEGO type:standard slot:1 autostart

from spike import PrimeHub, ColorSensor, Motor, MotorPair
from spike.control import wait_for_seconds, Timer, wait_until
from spike import App
from spike.operator import *
from hub import battery
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

def fluxCapacitor(time_ms, leftMotorSpeed, rightMotorSpeed):
    # Drive until the defined time elapses
    motorPair.start_tank(leftMotorSpeed,rightMotorSpeed)
    utime.sleep_ms(time_ms)
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

#print(sys.version)
#print(os.uname())
fleep(1500, 20, 20)
wait_for_seconds(1)
fleep(3000, -20, -20)
wait_for_seconds(1)
fleep(980, -20, -20)

# fluxCapacitor(1500, 40, 40)
# fluxCapacitor(500, -10, -10)
# megaBotsPrime.speaker.beep(80, 0.1)
# fluxCapacitor(500, -10, -10)
# megaBotsPrime.speaker.beep(80, 0.1)
# fluxCapacitor(500, -10, -10)
# megaBotsPrime.speaker.beep(80, 0.1)