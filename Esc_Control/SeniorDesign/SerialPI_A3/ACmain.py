from time import sleep
from ArduinoComms import ArduinoComm

a = ArduinoComm()

try:
    a.arm()
    while a.getArmed():
        a.write([1500,3000,1200,1400,1900,2100])
        sleep(1)
        a.write([1300,2300,2600,800,0000,3000])
        sleep(1)
except:
    a.disarm()
    a.cleanup()


