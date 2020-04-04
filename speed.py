#!/bin/python

import RPi.GPIO as GPIO
from multiprocessing import Pool, Process, Queue
import time
import atexit
from datetime import datetime



class Speed:
    def __init__(self):
        self.leftTicks = 0
        self.rightTicks = 0
        GPIO.setmode(GPIO.BCM)
        trigLeft = 4
        trigRight = 17
        GPIO.setup(trigLeft,GPIO.IN)
        GPIO.setup(trigRight,GPIO.IN)
        GPIO.add_event_detect(trigLeft,GPIO.RISING, callback=self.tickLeftWheel,bouncetime=10)
        GPIO.add_event_detect(trigRight,GPIO.RISING, callback=self.tickRightWheel,bouncetime=10)

    def tickLeftWheel(self,info):
        self.leftTicks += 1
    def tickRightWheel(self,info):
        self.rightTicks += 1




    def resetTicks(self):
        self.leftTicks = 0
        self.rightTicks = 0
        self.fasterSide = 0

    def getTicks(self):
        return (self.leftTicks,self.rightTicks)



