from communications.ArduinoComm import ArduinoComm
from sensory import getSensoryData
from time import sleep
from threading import Timer

class SubControl:

    debug = False;

    updateRate = 0.2 #rate in seconds

    def __init__(self, a=ArduinoComm(), init_target=[0] * 29, init_update=True):
        self.update = init_update
        self.target = init_target

        try:
            self.arduinoComm = a
        except:
            print("ERROR: SubSubControl: Cannot establish Arduino Communications.")
            exit(1)

        self.deadBand = self.arduinoComm.getDeadBand()

        try:
            self.sensory = getSensoryData()
        except:
            print("ERROR: Cannot establish Sensory")
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
        # x,y,z will be values (+/-)0-180 representing the degree difference between the target and the recieved infromation from IMU.
        x = 0
        y = 0
        z = 0
        #FIXME find out what how the coordinate data works to be able to calculate difference.
        returnDifference = [x,y,z]
        return returnDifference

    def getSpeeds(self):
        returnSpeeds = [self.deadBand] * 6
        #FIXME change Speeds to represent difference magnitude. Some sort of quadrateic.
        return returnSpeeds

    def setTarget(self, newTarget):
        self.target = newTarget

    def calTarget(self):
        self.target = self.sensory.getAllData()

    def getTarget(self):
        return self.target