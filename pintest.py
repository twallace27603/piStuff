import RPi.GPIO as GPIO
import time
import math
from multiprocessing import Pool, Process, Queue
import Queue as Q
import pins

GPIO.setmode(GPIO.BCM)
for trigger in triggers:
    GPIO.setup(trigger,GPIO.OUT)
    GPIO.output(trigger,False)
pin = pins.distance_trigger
GPIO.output(pin,True)
ans = input('Testing middle, click enter to continue')
GPIO.output(pin,False)
pin = pins.distance_trigger_left
GPIO.output(pin,True)
ans = input('Testing left, click enter to continue')
GPIO.output(pin,False)
pin = pins.distance_trigger_left
GPIO.output(pin,True)
ans = input('Testing left, click enter to continue')
GPIO.output(pin,False)
GPIO.cleanup()
