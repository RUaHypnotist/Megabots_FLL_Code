# LEGO type:standard slot:2 autostart

from spike import PrimeHub, LightMatrix, Button, StatusLight, ForceSensor, MotionSensor, Speaker, ColorSensor, App, DistanceSensor, Motor, MotorPair
from spike.control import wait_for_seconds, Timer
from spike.operator import greater_than
from math import *

#Initialization
megaBotsPrime = PrimeHub()

# Motor and Sensor Definitions
leftMotor = "A"
rightMotor = "E"
frontMotor = Motor("D")
backMotor = Motor("C")
leftColor = ColorSensor("B")
rightColor = ColorSensor("F")

motorPair = MotorPair(leftMotor, rightMotor)

#Test Moving
#driverPair.move(100, "degrees", 0, 40)
#wait_for_seconds(5)
#driverPair.move_tank(200, "degrees", 20, 20)

#M2 Oil Truck pull to base
#motorPair.move(100, "degrees", 0, 10)
#motorPair.move(400, "degrees", 0, 30)
#backMotor.run_for_degrees(180, 50)

#while True:
#    megaBotsPrime.light_matrix.write(rightColor.get_rgb_intensity())


megaBotsPrime.light_matrix.write(rightColor.get_rgb_intensity())
print("Testing White")
print("White RGB: " , rightColor.get_rgb_intensity())
print("White Reflected: " , rightColor.get_reflected_light())

wait_for_seconds(2)
megaBotsPrime.light_matrix.write("Change to Black")
wait_for_seconds(10)

megaBotsPrime.light_matrix.write(rightColor.get_rgb_intensity())
print("Testing Black")
print("Black RGB: " , rightColor.get_rgb_intensity())
print("Black Reflected: " , rightColor.get_reflected_light())