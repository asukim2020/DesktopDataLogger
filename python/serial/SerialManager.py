import serial
import threading
import copy
from python.serial.RequestApi import RequestApi as api

from python.serial.TimeUtil import TimeUtil


class SerialManager:
    # port = "/dev/ttyS0"
    port = "COM1"
    baud = 9600

    def __init__(self):
        super().__init__()

        # 객체 변수 선언
        self.ser = None
        self.line = []
        self.exitMeasureThread = False
        self.items = []

    def start(self):
        self.exitMeasureThread = True

        if self.ser is None:
            self.ser = serial.Serial(SerialManager.port, SerialManager.baud, timeout=0)
            self.ser.write(b"*S$")

            thread = threading.Thread(target=self.readThread)
            thread.start()

    def readThread(self):
        while self.exitMeasureThread:
            for c in self.ser.read():
                self.line.append(chr(c))

                if c == 10:
                    tmp = ''.join(self.line)

                    dic = {}
                    dic["data"] = tmp
                    dic["time"] = TimeUtil.getNewTimeByLong()
                    self.items.append(dic)
                    self.line.clear()

                    print(tmp, end='')

                if len(self.items) == 100:
                    copyItems = copy.deepcopy(self.items)
                    api.addMeasureItems(copyItems)
                    self.items.clear()



    def end(self):
        self.exitMeasureThread = False

        if self.ser is not None:
            self.ser.write(b"*T$")
            self.ser.close()
            self.ser = None


# Test Code
if __name__ == "__main__":
    manager = SerialManager()
    manager.start()
    # manager.end()