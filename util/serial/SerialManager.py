import serial
import asyncio

from util.eventbus.GlobalBus import GlobalBus, subscribe, Mode, threading
from util.eventbus.HashMapEvent import HashMapEvent


class SerialManager:
    port = "COM1"
    baud = 38400

    def __init__(self):
        super().__init__()

        # 객체 변수 선언
        self.ser = None
        self.line = []
        self.exitMeasureThread = False

    def start(self):
        self.exitMeasureThread = True
        if self.ser is None:
            self.ser = serial.Serial(SerialManager.port, SerialManager.baud, timeout=0)
        thread = threading.Thread(target=self.readThread)
        thread.start()

    def readThread(self):
        self.ser.write(b"*S$")

        while self.exitMeasureThread:
            for c in self.ser.read():
                GlobalBus.register(self)
                self.line.append(chr(c))

                if c == 10:
                    event = HashMapEvent()
                    event.map[SerialManager.toString()] = SerialManager.toString()
                    event.map["line"] = self.line

                    GlobalBus.sBus.post(event)
                    # self.printLine(self.line)

                    self.line.clear()

    def end(self):
        self.exitMeasureThread = False

        if self.ser is not None:
            self.ser.write(b"*T$")
            self.ser.close()
            self.ser = None

    @staticmethod
    def printLine(s):
        tmp = ''.join(s)

        # 출력!
        print(tmp)

    @staticmethod
    def toString():
        return "SerialManager"

    @subscribe(threadMode=Mode.POSTING, onEvent=HashMapEvent)
    def func(self, event):
        serialManager = event.map.get(SerialManager.toString())
        if serialManager is not None:
            line = event.map.get("line")

            if line is not None:
                tmp = ''.join(line)
                print(tmp)


# Test Code
if __name__ == "__main__":
    manager = SerialManager()
    manager.start()
