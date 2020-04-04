import wheels 
from sensors import Sensors
import configuration
import time
import math

class Robot:
    def __init__(self):        
        self.w = wheels.wheels()
        self.s = Sensors()
        self.config = configuration.config()
        self.w.setConfig(self.config)
        self.s.setConfig(self.config)
        self.s.calibration = True

    def point(self,goal):
        heading = self.s.getHeading()
        power = 0
        newPower = 0
        if heading > goal:
            self.w.setSpeed(0, wheels.Direction.Right)
        else:
            self.w.setSpeed(0,wheels.Direction.Left)
        delta = abs(heading - goal)

        while delta>2:
            if delta > 90:
                power = int(self.minPower * 1.5)
                sec = .25
            elif delta > 30:
                power = int(self.minPower * 1.25)
                sec = .1
            else:
                sec = .05
                power = self.minPower
            self.w.pulse(seconds=sec, bump=power)
            time.sleep(.05)
            heading = self.s.getHeading()
            delta = abs(heading - goal)

    def calibrateCompassNWheels(self):
        #First read seems wonky so this is a throw away
        north = self.s.getReadings()
        time.sleep(.5)

        #Actual first reading, also used for north
        north = self.s.getReadings()

        #Find minimum spin level - > 10 x at .1 second rate
        x0 = north[0]
        x1 = x0
        self.minPower = 0
        bump = 5
        self.w.setSpeed(0,wheels.Direction.Right)
        while abs(x1 - x0) < 10:
            x0 = x1
            self.minPower += bump
            self.w.pulse(seconds = .1, bump = self.minPower)
            time.sleep(.1)
            x1 = self.s.getReadings()[0]
        print("Minimum level: {}".format(self.minPower))

        self.w.setSpeed(self.minPower,wheels.Direction.Right)
        for i in range(200):
            readings = self.s.getReadings()
            time.sleep(.05)
        print("{}\t{}\t{}\t{}".format(self.s.minx, self.s.maxx,self.s.miny,self.s.maxy))
        self.s.setNorth(north[0],north[1])
        self.w.setSpeed(0,wheels.Direction.Left)
        self.point(0)


if __name__=="__main__":
    robot = Robot()
    robot.calibrateCompassNWheels()
    robot.point(90)
    time.sleep(1)
    robot.point(180)
    time.sleep(1)
    robot.point(270)
    time.sleep(1)
    robot.point(360)
    time.sleep(1)
