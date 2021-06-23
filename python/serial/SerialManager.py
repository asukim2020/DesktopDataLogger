import serial
import threading
import copy
from python.serial.RequestApi import RequestApi as api

from python.serial.TimeUtil import TimeUtil


class SerialManager:
    # port = "/dev/ttyS0"
    # port = "/dev/ttyAMA0"
    port = "COM1"
    baud = 38400

    def __init__(self):
        super().__init__()

        # 객체 변수 선언
        self.ser = None
        self.line = []
        self.exitMeasureThread = False
        self.items = []
        self.emergencyFlag = False
        self.safetyCount = 0

        self.abnormalData = 0
        self.alwaysSaveCount = 500

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

                    while len(self.items) > self.alwaysSaveCount \
                            and not self.emergencyFlag:
                        self.items.pop(0)

                    self.line.clear()

                    # print(tmp, end='')

                    tmp = tmp.replace("+", ",")
                    tmp = tmp.replace("-", ",-")
                    tmp = tmp.replace("*", "")
                    tmp = tmp.replace("$", "")
                    items = tmp.split(",")

                    print("%d, %d, %d, %d, %d"
                          % (
                              int(items[1]),
                              int(items[2]),
                              int(items[3]),
                              int(items[4]),
                              int(items[5])
                          )
                          )

                    # if int(items[2]) < self.abnormalData \
                    #         and not self.emergencyFlag:
                    #     self.emergencyFlag = True
                    #     print("지진 발생")
                    #
                    # if self.emergencyFlag:
                    #     if int(items[2]) < self.abnormalData:
                    #         self.safetyCount = 0
                    #     else:
                    #         self.safetyCount += 1
                    #
                    #     if self.safetyCount > self.alwaysSaveCount:
                    #         print("지진 종료")
                    #         self.emergencyFlag = False
                    #
                    # if self.emergencyFlag and len(self.items) >= 100:
                    #     copyItems = copy.deepcopy(self.items)
                    #     api.addMeasureItems(copyItems)
                    #     self.items.clear()
                    #     print("데이터 업로드")
                        # TODO: - 정시 측정 시에는 self.emergencyFlag 끄고 items 클리어 후 aws에 업로드





                # if len(self.items) >= 100:
                    # copyItems = copy.deepcopy(self.items)
                    # api.addMeasureItems(copyItems)
                    # self.items.clear()



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