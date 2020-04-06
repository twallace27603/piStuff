
#!/bin/python

import RPi.GPIO as GPIO
import time
import math
from multiprocessing import Pool, Process, Queue
import Queue as Q
import pins
class Distance:
    def __init__(self, trigs,echo):
        for trig in trigs:
            GPIO.setup(trig,GPIO.OUT)
            GPIO.output(trig,False)
        GPIO.setup(echo,GPIO.IN)
        self.trigs = trigs
        self.echo = echo
        
        
        
    def getDistance(self,trials,timeout):
        triggers = self.trigs
        sensor = self.echo
        avgHigh = int(math.floor(trials/2))
        if(avgHigh == trials/2):
            avgLow = avgHigh - 1
        else:
            avgLow = avgHigh
        cont = True
        startTime = time.time()
        distances = []
        print(trials)

        for trigger in triggers:
            times = []
            print(trigger)
            for trial in range(1,trials):
                high = False
                low = False
                highTime = time.time()
                lowTime = time.time()
                startTime = time.time()
                cont = True
                GPIO.output(trigger,True)
                time.sleep(0.00001)
                GPIO.output(trigger,False)
                while cont: 
                   reading = GPIO.input(sensor)
                   rt = time.time()
                   if reading == 1:
                       high = True
                   else:
                       if high == False:
                           highTime = rt
                       else:
                           low = True
                           lowTime = rt
                   cont = (low == False) and ((time.time() - startTime) < timeout)
                if low:
                    print("Trigger {} trial {} had a time of {}".format(trigger, trial,(lowTime-highTime)))
                else:
                    print("Trigger {} trial {} did not capture a time".format(trigger,trial))
                       
                times.append(lowTime - highTime)
            times.sort()
            distances.append((times[avgHigh] + times[avgLow]) / 2 *17150)
        return distances

if __name__ == '__main__':
    print("hey")
    timeout = 1
    retries = 5
    trigs = (pins.distance_trigger,pins.distance_trigger_left,pins.distance_trigger_right,)
    echo = pins.distance_read
    GPIO.setmode(GPIO.BCM)
    d = Distance(trigs, echo)
    distances = d.getDistance(retries,timeout)
    print(distances)
    GPIO.cleanup()


