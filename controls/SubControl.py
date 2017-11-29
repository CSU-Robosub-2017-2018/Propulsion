from communications.ArduinoComm import ArduinoComm
from time import sleep

class SubControl:

    debug = False;

    updateRate = 0.2 #rate in seconds

    def __init__(self, init_target=[0] * 29, update=True):
        self.update = update
        self.target = init_target
        try:
            self.arduinoComm = ArduinoComm()
        except:
            print("ERROR: Cannot establish Arduino Communications.")
            exit(1)
        self.updateMotors()

    def updateMotors(self):
        #FIXME write update motors system.
