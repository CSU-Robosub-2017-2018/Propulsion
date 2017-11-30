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
                sleep(5)
                while a.getArmed():
                    a.writeMicroSeconds([1500, 3000, 1200, 1400, 1900, 2100])
                    sleep(1)
                    a.writeMicroSeconds([1300, 2300, 2600, 800, 0000, 3000])
                    sleep(1)

            except:
                a.disarm()
except:
    a.cleanup()
