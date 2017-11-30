from time import sleep
from communications.ArduinoComm import ArduinoComm
from controls.SubControl import SubControl

a = ArduinoComm()
s = SubControl(a)

a.arm()
s.updateMotors()
