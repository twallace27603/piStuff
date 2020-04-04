#!/usr/bin/python
import smbus
import time
import math
import distance
import pins
import RPi.GPIO as GPIO
import wheels
import compass
from datetime import datetime

class Sensors():
    def __init__(self, wheels, compass, distance):

        ##Set up compass
        self.compass = compass
        ##set up distance
        self.distance = distance
        self.distanceTrials = 5
        self.distanceTimeout = 1

        ##attach to wheels
        self.wheels = wheels

    def setConfig(self,config):
        self.config = config
        

    

    def getReadings(self):
        heading = self.compass.getHeading()
        compassReadings = self.compass.getReadings()
 
        distance = self.distance.getDistance(self.distanceTrials, self.distanceTimeout)
        dt = datetime.now().strftime('%H:%M:%S')
        return (dt,heading,compassReadings, distance,self.wheels.getTicks())


    def test(self):

        command = raw_input('Command:')
        while command != 'quit':
            print(self.getReadings())
            command = raw_input("Command:")


if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    c = compass.Compass()
    c.calibration = True
    c.firstReading = False
    c.getReadings()
    c.getHeading()
    echos = (pins.distance_read,)
    d = distance.Distance(pins.distance_trigger, echos)
    w = wheels.Wheels()
    s = Sensors(w,c,d)
    s.test()

        

    
    
