
#!/bin/python

import RPi.GPIO as GPIO
import time
from multiprocessing import Pool, Process, Queue
import Queue as Q

class Distance:
    def __init__(self,trig,echos,timeout):
        GPIO.setup(trig,GPIO.OUT)
        self.sensors = []
        self.timeout = timeout
        self.trig = trig
        GPIO.output(trig,False)
        for echo in echos:
            GPIO.setup(echo,GPIO.IN)
            self.sensors.append([echo,0,0,time.time(),time.time(),0])
        
        
    def getDistance(self,q):

        sensors = self.sensors
        timeout = self.timeout
        trig = self.trig
        for sensor in sensors:
            sensor[1] = 0
            sensor[2] = 0
            sensor[3] = time.time()
            sensor[4] = time.time()

        
##        print("Begin")
        cont = True
        startTime = time.time()
        count = len(sensors)
        flag = 0

        GPIO.output(trig,True)
        time.sleep(0.00001)
        GPIO.output(trig,False)
        
        while cont:
            for sensor in sensors:
               reading = GPIO.input(sensor[0])
               rt = time.time()
               if reading == 1:
                   sensor[1]=1
               else:
                   if sensor[1] == 0:
                       sensor[3] = rt
                   elif sensor[2] == 0:
                       sensor[2] = 1
                       sensor[4] = rt
                       flag += 1
            cont = (flag < count) and ((time.time() - startTime) < timeout)
        distances = []
        for sensor in sensors:
            if(sensor[2] == 1):
                distances.append((sensor[4] - sensor[3]) *17150)
            else:
                distances.append(-1)
        q.put(distances)
##        print("End")
 
            
    ##    while GPIO.input(echo)==0:
    ##        pulse_start = time.time()
    ##    while GPIO.input(echo)==1:
    ##        pulse_end = time.time()
    ##    pulse_duration = pulse_end - pulse_start
    ##    distance = pulse_duration*17150
    ##    distance = round(distance,2)
    ##    q.put(distance)
    ##    print("Recorded")
    ##    GPIO.cleanup()


GPIO.setmode(GPIO.BCM)
q = Queue()
#echos = (22,18,27)
echos = (27,)
ds = Distance(23,echos,2)
##p = Process(target=ds.getDistance, args=(q,))
##p.start()
ds.getDistance(q)
loops = 10
trim = 2
bottom = trim - 1
top = loops - 2 * trim + 1
loop = 0
distances = []
for e in echos:
    distances.append([])
startTime = time.time()
while loop < loops:
    if not q.empty():
        result = q.get(False)
        for lcv in range(len(result)):
            distances[lcv].append(result[lcv])
        loop += 1
##        p.start()
        ds.getDistance(q)
    else:
        print("No response")
        time.sleep(.05)
endTime = time.time()

print("Time to process: {} seconds.".format(endTime-startTime))

output = []
for distance in distances:
    distance.sort()
    distance = distance[bottom:top]
    output.append(float(sum(distance)) / max(len(distance), 1))
print(output)
GPIO.cleanup()


