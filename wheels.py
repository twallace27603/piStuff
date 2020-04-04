from enum import Enum
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
import time
import atexit
from datetime import datetime

import RPi.GPIO as GPIO
from multiprocessing import Pool, Process, Queue


Direction = Enum('Forward','Reverse','Spin','Left','Right','None')

class Wheels:
    def __init__(self):
        self.lc = 100 #Loop count
        self.ld = .02 #Loop delay
        self.mh = Adafruit_MotorHAT(addr=0x60)
        self.speed = 0
        self.direction = Direction.None
        atexit.register(self.turnOffMotors)
        self.rightWheel = self.mh.getMotor(2)
        self.leftWheel = self.mh.getMotor(1)
        self.minPower = 55
        self.leftTicks = 0
        self.rightTicks = 0
        self.fasterSide = 0
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

    def setConfig(self,config):
        self.config = config
        self.lc = config.wheelsLoopCount
        self.ld = config.wheelsLoopDelay
        self.mh = Adafruit_MotorHAT(addr=config.wheelsAddr)
        self.speed = 0
        self.direction = Direction.None
        self.minPower = config.wheelsMinPower
        self.rightWheel = self.mh.getMotor(config.wheelsRight)
        self.leftWheel = self.mh.getMotor(config.wheelsLeft)


    def turnOffMotors(self):
        self.mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
        self.mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
        self.mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
        self.mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)

    def setSpeed(self,speed, direction):
        if((self.speed>0) and (speed>0) and (self.direction != direction)):
            self.setSpeed(0,self.direction)
            time.sleep(.1)
        if (direction!=self.direction):
            if direction == Direction.Forward:
                self.rightWheel.run(Adafruit_MotorHAT.FORWARD)
                self.leftWheel.run(Adafruit_MotorHAT.FORWARD)
            elif direction == Direction.Reverse:
                self.rightWheel.run(Adafruit_MotorHAT.BACKWARD)
                self.leftWheel.run(Adafruit_MotorHAT.BACKWARD)
            elif (direction == Direction.Spin) or (direction == Direction.Left):
                self.rightWheel.run(Adafruit_MotorHAT.FORWARD)
                self.leftWheel.run(Adafruit_MotorHAT.BACKWARD)
            elif direction == Direction.Right:
                self.rightWheel.run(Adafruit_MotorHAT.BACKWARD)
                self.leftWheel.run(Adafruit_MotorHAT.FORWARD)
            elif direction == Direction.None:
                self.turnOffMotors()
                return
                
        self.leftWheel.setSpeed(speed)
        self.rightWheel.setSpeed(speed)
        self.speed = speed
        self.leftSpeed = speed
        self.rightSpeed = speed
        self.direction = direction

    def correct(self):
        if self.leftTicks == self.rightTicks:
            self.fasterSide = 0
            if self.leftSpeed != self.rightSpeed:
                self.leftSpeed = self.speed
                self.rightSpeed = self.speed
                self.leftWheel.setSpeed(self.speed)
                self.rightWheel.setSpeed(self.speed)
        elif self.leftTicks > self.rightTicks:
            if self.fasterSide == 1:
                self.fasterSide = -1
            elif abs(self.speed - self.leftSpeed) > abs(self.speed - self.rightSpeed):
                self.rightSpeed += 5
                self.rightWheel.setSpeed(self.rightSpeed)
            else:
                self.leftSpeed -= 5
                self.leftWheel.setSpeed(self.leftSpeed)
        else:
            if self.fasterSide == -1:
                self.fasterSide = 1
            elif abs(self.speed - self.leftSpeed) > abs(self.speed - self.rightSpeed):
                self.rightSpeed -= 5
                self.rightWheel.setSpeed(self.rightSpeed)
            else:
                self.leftSpeed += 5
                self.leftWheel.setSpeed(self.leftSpeed)


    def slowStop(self):
        speed = self.speed
        direction = self.direction
        while (speed > 30):
            speed -= 30
            self.setSpeed(speed,direction)
            time.sleep(.05)
        self.setSpeed(0,direction)

    def pulse(self,seconds=.25,bump=20):
        self.rightWheel.setSpeed(self.speed + bump)
        self.leftWheel.setSpeed(self.speed + bump)
        time.sleep(seconds)
        self.rightWheel.setSpeed(self.speed)
        self.leftWheel.setSpeed(self.speed)
        
    def resetTicks(self):
        self.leftTicks = 0
        self.rightTicks = 0
        self.fasterSide = 0

    def getTicks(self):
        return (self.leftTicks,self.rightTicks)

    def testRun(self,speed, wait, direction):
        self.setSpeed(0,direction)
        self.resetTicks()
        self.setSpeed(speed,direction)
        t1 = datetime.now()
        while (datetime.now() - t1).total_seconds() < wait:
            time.sleep(.1)
            self.correct()
        print("Speed: {} \tDirection: {}\tLeft: {}\tRight: {}".format(speed,direction,self.leftTicks,self.rightTicks))
        self.slowStop()
        time.sleep(1)

    def test(self):
        speed = 150
        wait = 3
        self.testRun(speed,wait,Direction.Forward)
        self.testRun(speed,wait,Direction.Reverse)
        self.testRun(speed,wait,Direction.Spin)

        
if __name__ == '__main__':
    w = wheels()
    w.test()
    w.turnOffMotors()

