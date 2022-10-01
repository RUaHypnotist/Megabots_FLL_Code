# LEGO type:standard slot:2 autostart

from spike import PrimeHub, LightMatrix, Button, StatusLight, ForceSensor, MotionSensor, Speaker, ColorSensor, App, DistanceSensor, Motor, MotorPair
from spike.control import wait_for_seconds, Timer
from spike.operator import greater_than
from math import *

#Initialization
hub = PrimeHub()
driverPair = MotorPair("A", "E")

#Test Moving
driverPair.move(100, "degrees", 0, 40)
wait_for_seconds(5)
driverPair.move_tank(200, "degrees", 20, 20)