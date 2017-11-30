from communications.ArduinoComm import ArduinoComm
#from sensory import getSensoryData
from time import sleep
from threading import Timer
import math

class SubControl:

    debug = False;

    updateRate = 0.2 #rate in seconds

    def __init__(self, a=ArduinoComm(), init_target=[0] * 29, init_update=True):
        self.update = init_update
        self.target = init_target

        try:
            self.arduinoComm = a
        except:
            print("ERROR: SubControl: Cannot establish Arduino Communications.")
            exit(1)

        self.deadBand = self.arduinoComm.getDeadBand()

        try:
            #self.sensory = getSensoryData()
            print("Jo-Bob")
        except:
            print("ERROR: SubControl: Cannot establish Sensory")
            exit(1)

        self.updateMotors()

    def updateMotors(self):
        if not self.arduinoComm.armed:
            print("WARNING: SubControl: Sub not armed, cannot update")
        elif not self.update:
            print("WARNING: SubControl: update was not set to TRUE, cannot update")
        else:
            # FIXME write update motors system.
            if self.debug:
                print("UpdateMotors: ")
            self.arduinoComm.writeMicroSeconds(self.getSpeeds())
            Timer(self.updateRate,self.updateMotors).start() #makes new thread that calls updateMotors every updateRate seconds

    def getDifference(self):
        # x,y,z will be values (+/-)0-pi representing the radian difference between the target and the recieved infromation from the IMU.
        x = int(input("x:"))
        y = int(input("y:"))
        z = int(input("z:"))
        #FIXME find out what how the coordinate data works to be able to calculate difference.
        returnDifference = [x,y,z]
        return returnDifference

    def getSpeeds(self):
        returnSpeeds = [self.deadBand] * 6
        difference = self.getDifference()
        i = 0;
        for d in difference:
            returnSpeeds[i] = returnSpeeds[i] + round(8.06*math.pow(d,3))
            returnSpeeds[i+1] = returnSpeeds[i+1] - round(8.06*math.pow(d,3))
            i = i + 2
        #FIXME change Speeds to represent difference magnitude. Some sort of quadrateic.
        return returnSpeeds

    def setTarget(self, newTarget):
        self.target = newTarget

    def calTarget(self):
        self.target = self.sensory.getAllData()

    def getTarget(self):
        return self.target