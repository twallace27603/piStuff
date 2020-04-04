import wheels
import sensors
import configuration
import time
import math
import json

w = wheels.wheels()
s = sensors.Sensors()
config = configuration.config()
w.setConfig(config)
s.setConfig(config)
s.calibration = True

#General calibration of turning and direction
def generalCalibration():
    #First read seems wonky so this is a throw away
    north = s.getReadings()
    time.sleep(.5)

    #Actual first readiing, also used for north
    north = s.getReadings()

    #Find minimum spin level - > 10 x at .1 second rate
    x0 = north[0]
    x1 = x0
    minPower = 0
    bump = 5
    w.setSpeed(0,wheels.Direction.Right)
    while abs(x1 - x0) < 10:
        x0 = x1
        minPower += bump
        w.pulse(seconds = .1, bump = minPower)
        time.sleep(.1)
        x1 = s.getReadings()[0]
    print("Minimum level: {}".format(minPower))

    w.setSpeed(minPower,wheels.Direction.Right)
    for i in range(200):
        #w.pulse(seconds=.1,bump=50)
        readings = s.getReadings()
        time.sleep(.05)
    print("{}\t{}\t{}\t{}".format(s.minx, s.maxx,s.miny,s.maxy))
    s.setNorth(north[0],north[1])
    w.setSpeed(0,wheels.Direction.Left)

    #for i in range(100):
    #    w.pulse(seconds=.1,bump=50)
    #    print("{};{}".format(i,s.getHeading()))
    #    time.sleep(.1)

    print("Heading north")
    heading = s.getHeading()
    goal = 0.0
    power = 0
    newPower = 0
    if heading > goal:
        w.setSpeed(0, wheels.Direction.Right)
    else:
        w.setSpeed(0,wheels.Direction.Left)
    delta = abs(heading - goal)

    while delta>2:
        if delta > 90:
            power = int(minPower * 1.5)
            sec = .25
        elif delta > 30:
            power = int(minPower * 1.25)
            sec = .1
        else:
            sec = .05
            power = minPower
        w.pulse(seconds=sec, bump=power)
        time.sleep(.05)
        heading = s.getHeading()
        delta = abs(heading - goal)
        print("{}\t{}\t{}".format(goal,heading,delta))

    print('Moving North')
    w.setSpeed(minPower+20,wheels.Direction.Forward)
    time.sleep(1.5)
    w.setSpeed(0,wheels.Direction.Left)
    print('Turning South')
    heading = s.getHeading()
    goal = 100
    delta = abs(heading - goal)
    while delta>2:
        if delta > 90:
            power = int(minPower * 1.5)
            sec = .25
        elif delta > 30:
            power = int(minPower * 1.25)
            sec = .1
        else:
            sec = .05
            power = minPower
        w.pulse(seconds=sec, bump=power)
        time.sleep(.05)
        heading = s.getHeading()
        delta = abs(heading - goal)
        print("{}\t{}\t{}".format(goal,heading,delta))
    print('Continuing to turn south')
    heading = s.getHeading()
    goal = 180
    delta = abs(heading - goal)
    while delta>2:
        if delta > 90:
            power = int(minPower * 1.5)
            sec = .25
        elif delta > 30:
            power = int(minPower * 1.25)
            sec = .1
        else:
            sec = .05
            power = minPower
        w.pulse(seconds=sec, bump=power)
        time.sleep(.05)
        heading = s.getHeading()
        delta = abs(heading - goal)
        print("{}\t{}\t{}".format(goal,heading,delta))

    print('Moving south')
    w.setSpeed(int(minPower*1.5),wheels.Direction.Forward)
    time.sleep(1.5)
    w.setSpeed(0,wheels.Direction.Left)
        
    print('Home!')

def collectCompassReadings():
    speed = 150
    w.setSpeed(speed,wheels.Direction.Forward)
    time.sleep(1)
    w.setSpeed(0,wheels.Direction.Forward)
    w.resetTicks()
    w.setSpeed(speed,wheels.Direction.Spin)
    readings = []
    for i in range(200):
        time.sleep(.01)
        w.correct()
        readings.append(s.getReadings())
        if (i % 20 == 0):
            print("Completed {} readings".format(i))
    w.setSpeed(0,wheels.Direction.Spin)
    fileName="./compassreadings.csv"
    with open(fileName,'w') as output:
        for reading in readings:
            output.write("{},{},{}\n".format(reading[0],reading[1],reading[2]))
        #json.dump(readings,output)
    
collectCompassReadings()    
w.turnOffMotors()
