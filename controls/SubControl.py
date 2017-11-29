from communications.ArduinoComm import ArduinoComm
from time import sleep

class SubControl:

    debug = False;

    def __init__(self, init_target=[0] * 29):
        self.target = init_target
        try:
            arduinoComm = ArduinoComm()
        except:
            print("ERROR: Cannot establish Arduino Communicaitons.")
            exit(1)
        updateMotors();




