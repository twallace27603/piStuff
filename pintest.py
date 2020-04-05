import RPi.GPIO as GPIO
import time
import math
from multiprocessing import Pool, Process, Queue
import Queue as Q
import pins

pin = pins.distance_trigger
GPIO.setup(pin,GPIO.OUT)
GPIO.output(pin,True)
time.sleep(60.0)
GPIO.output(pin,False)
GPIO.cleanup()
