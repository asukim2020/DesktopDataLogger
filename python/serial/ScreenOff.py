import threading
import time
import RPi.GPIO as GPIO

class ScreenOff:

    def startThread(self):
        thread = threading.Thread(target=self.screenOff)
        thread.start()

    def screenOff(self):
        time.sleep(3600)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(34, GPIO.OUT)
        GPIO.output(34, GPIO.LOW)