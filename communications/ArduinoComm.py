try:
    import RPi.GPIO as GPIO
    import serial
    from threading import Timer
    from time import sleep
except:
    import tests.serial as serial
    from tests.rpidevmocks import MockGPIO
    GPIO = MockGPIO()
    from threading import Timer
    from time import sleep

class ArduinoComm:

    debug = True

    error = False

    deadBand = 1500 #motor dead band
    Uplimit = 1750 #desired upper uS limit
    Lowlimit = 1250 #desired lower uS limit
    hardUpLimit = 2000 #max upper uS limit
    hardLowLimit = 1000 #min lower us limit

    updateRate = 0.2 #rate in seconds

    errorGpioPin = 18 #FIXME get a good gpio pin

    def __init__(self, update=False):
        self.update = update
        self.armed = False
        self.speeds = [self.deadBand] * 6 #Motor uSecond values: [x1,x2,y1,y2,z1,z2]
        try:
            self.ser = serial.Serial("/dev/ttyACM0", 19200)
        except:
            print("ERROR: ArduinoComm: Cannot connect to serial port!")
            exit(1)
        try:
            GPIO.setmode(GPIO.BCM)
            # GPIO gpioPin set up as an input, pulled down, connected to 3V3 on error
            GPIO.setup(self.errorGpioPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            # when a rising edge is detected on port gpioPin, regardless of whatever
            # else is happening in the program, the function clearError will be run
            GPIO.add_event_detect(self.errorGpioPin, GPIO.RISING, callback=self.error, bouncetime=300)
        except:
            print("ERROR: ArduinoComm: Cannot setup GPIO Interrupt!")


    def initESC(self):
        #FIXME: write esc initialization
        self.debug = False #Temporary call to make code compile. REMOVE when fixing fixme.
        
    def getArmed(self):
        return self.armed

    def writeMicroSeconds(self, newSpeeds):
        if len(newSpeeds) != len(self.speeds):
            print("WARNING: ArduinoComm: new speed arrays lengths don't match")
        elif self.armed:
            for e in range(0, len(self.speeds)):
                                if newSpeeds[e] > self.Uplimit:
                                        newSpeeds[e] = self.Uplimit
                                        if self.debug:
                                            print("WARNING: input exceeded upper limit")
                                if newSpeeds[e] < self.Lowlimit:
                                        newSpeeds[e] = self.Lowlimit
                                        if self.debug:
                                            print("WARNING: input exceeded lower limit")
            self.speeds = newSpeeds
            returnVal = ",".join(str(e) for e in self.speeds)
            self.ser.write(returnVal.encode())
            print("ArdiunoComm: Write: " + returnVal)
        else:
            print("ERROR: ArduinoComm: cannot write while motors are not armed.")

    def updateMicroSeconds(self):
        if not self.armed:
            print("WARNING: ArduinoComm: not armed, cannot update")
        elif not self.update:
            print("WARNING: ArduinoComm: update was not set to TRUE, cannot update")
        else:
            returnVal = ",".join(str(e) for e in self.speeds)
            self.ser.write(returnVal.encode())
            if self.debug:
                print("update: " + returnVal)
            Timer(self.updateRate,self.updateMicroSeconds).start() #makes new thread that calls update every updateRate seconds

    def arm(self):
        self.ser.write("1".encode())
        if self.debug:
            print("ARMED")
        self.armed = True
        self.updateMicroSeconds()

    def disarm(self):
        self.ser.write("0".encode())
        if self.debug:
            print("DISARMED")
            #self.ser.getCount() #testing off of arduino with custom serial class
        self.armed = False

    def getSpeed(self):
        return self.speeds

    def getDeadBand(self):
        return self.deadBand

    def getUpLimit(self):
        return self.Uplimit

    def getLowLimit(self):
        return self.Lowlimit

    def error(self, extra):
        #FIXME: handle errors
        if self.debug:
            print("ArduinoComm: Error Detected")
        self.write([deadBand] * 6)
        self.armed = False
        self.error = True
        self.ser.write("2".encode())

    def getError(self):
        return self.error

    def clearError(self):
        self.error = False

    def cleanup(self):
        GPIO.cleanup()


