from time import sleep
from communications.ArduinoComm import ArduinoComm
from controls.SubControl import SubControl

a = ArduinoComm()
s = SubControl(a)


try:
    while True:
        s = (int)(input("Type 1: "))
        if s == 1:
            try:
                a.arm()
                s.updateMotors()
                while a.getArmed():
                    print(",".join(str(e) for e in a.getSpeed()))
            except:
                a.disarm()
except:
    a.cleanup()
