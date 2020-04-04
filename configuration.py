import json
import os.path
import sys
class config:

    def __init__(self):
        self.configFile = 'config.json'
        if os.path.exists(self.configFile):
            self.load()
        else:
            self.compassMaxX = 0
            self.compassMinX = 0
            self.compassMaxY = 0
            self.compassMinY = 0
            self.compassNorth = 0
            self.wheelsLoopCount = 100
            self.wheelsLoopDelay = .02
            self.wheelsAddr = 0x60
            self.wheelsMinPower = 55
            self.wheelsRight = 4
            self.wheelsLeft = 1
            

    def save(self):
        f = open(self.configFile,'w')
        json.dump(self.__dict__,f, indent = 4)
        f.close()

    def load(self):
        f = open(self.configFile,'r')
        self.__dict__ = json.load(f)
        f.close()
            
