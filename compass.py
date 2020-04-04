import smbus
import time
import math
import distance
import pins
import RPi.GPIO as GPIO

class Compass():
    def __init__(self):

        ##Set up compass
        self.address = 0x1e
        self.bus = smbus.SMBus(1)
        #self.bus.write_byte_data(self.address,0,0xd0)
        #self.bus.write_byte_data(self.address,2,0x01)
        self.x = 0
        self.y = 0
        self.z = 0
        self.minx = 0
        self.maxx = 0
        self.miny = 0
        self.maxy = 0
        self.minz = 0
        self.maxz = 0
        self.firstReading = True
        self.calibration = False
        self.north = 0

    def setConfig(self,config):
        self.config = config
        
    def setNorth(self,x1,y1):
        self.north = self.__calculateHeading__(x1,y1,False)
        return self.north

    def getHeading(self):
        (x1,y1,z1) = self.getReadings()
        return self.__calculateHeading__(x1,y1,True)

    def __calculateHeading__(self,x1,y1,northOffset):
        x = -1.0 + 2.0 * float(x1 - self.minx) / float(self.maxx - self.minx)
        y = -1.0 + 2.0 * float(y1 - self.miny) / float(self.maxy - self.miny)
        d = math.degrees(math.atan2(y,x))
        if northOffset:
            d -= self.north
        if d < 0:
            d = 360.0 + d
        return d

    

    def getReadings(self):
        retries = 0
        retry = True
        while retry:
            try:
                self.bus.write_byte_data(self.address,2,0x10)
                time.sleep(.01)
                self.bus.write_byte_data(self.address,2,0x01)
                time.sleep(.05)
                x0 = self.bus.read_byte_data(self.address,3)
                x1 = self.bus.read_byte_data(self.address,4)
                y0 = self.bus.read_byte_data(self.address,5)
                y1 = self.bus.read_byte_data(self.address,6)
                z0 = self.bus.read_byte_data(self.address,7)
                z1 = self.bus.read_byte_data(self.address,8)
                self.x = self.twosCompliment(x0,x1)
                #Currently the Y axis reports in the z register
                self.y = self.twosCompliment(z0,z1)
                self.z = self.twosCompliment(y0,y1)
                if self.calibration:
                    if self.firstReading:
                        self.minx = self.x
                        self.maxx = self.x
                        self.miny = self.y
                        self.maxy = self.y
                        self.minz = self.z
                        self.maxz = self.z
                        self.firstReading = False
                    else:
                        if self.x > self.maxx:
                            self.maxx = self.x
                        elif self.x < self.minx:
                            self.minx = self.x
                    
                        if self.y > self.maxy:
                            self.maxy = self.y
                        elif self.y < self.miny:
                            self.miny = self.y
                    
                        if self.z > self.maxz:
                            self.maxz = self.z
                        elif self.z < self.minz:
                            self.minz = self.z
                retry = False
            except IOError:
                retries += 1
                if retries > 3:
                    print("Encountered unrecoverable I/O error communicating with the compass")
                    retry = False
                time.sleep(.1)
        return (self.x, self.y, self.z)

    def twosCompliment(self,msb,lsb):
        value = msb * 256 + lsb
        if value > 0x8000:
            value -= 0x10000
        #return -(value & mask) + (value & ~mask)
        return value

    def test(self):
        command = raw_input('Command:')
        while command != 'quit':
            print(self.getReadings())
            print(self.getHeading())
            command = raw_input("Command:")

if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    c = Compass()
    c.calibration = True
    c.firstReading = False
    c.test()
