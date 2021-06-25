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
    saveBufferTime = 30
    accelIntervalPerSec = 100
    slopeIntervalPerSec = 1

    # TODO: - 시간 단위 지정도 추가

    accelMeasureMin = 5
    slopeMeasureMin = 5

    def __init__(self):
        super().__init__()

        # 객체 변수 선언
        self.serial = None
        self.line = []
        self.exitMeasureThread = False

        self.emergencyFlag = False
        self.safetyCount = 0
        self.abnormalData = 0
        self.emergencyFile = None

        self.requestFlag = False
        self.requestFile = None
        self.requestCount = 0

        self.accelItems = []
        self.accelCount = 1
        self.accelTimeCheckCount = 0
        self.accelInterval = 100 / SerialManager.accelIntervalPerSec
        self.accelSaveCount = SerialManager.saveBufferTime * SerialManager.accelIntervalPerSec
        self.accelFile = None
        self.accelDiff = 0.0

        self.slopeItems = []
        self.slopeCount = 1
        self.slopeTimeCheckCount = 0
        self.slopeInterval = 100 / SerialManager.slopeIntervalPerSec
        self.slopeSaveCount = SerialManager.saveBufferTime * SerialManager.slopeIntervalPerSec
        self.slopeFile = None
        self.slopeDiff = 0.0

        self.stringList = []

    def start(self):
        self.exitMeasureThread = True

        if self.serial is None:
            self.serial = serial.Serial(SerialManager.port, SerialManager.baud, timeout=0)
            self.serial.write(b"*S$")

            thread = threading.Thread(target=self.readThread)
            thread.start()

    def readThread(self):
        while self.exitMeasureThread:
            for c in self.serial.read():
                self.line.append(chr(c))

                if c == 10:
                    tmp = ''.join(self.line)

                    measureItem = {}
                    self.line.clear()

                    # print(tmp, end='')

                    tmp = tmp.replace("+", " , ")
                    tmp = tmp.replace("-", " , -")
                    tmp = tmp.replace("*", "")
                    tmp = tmp.replace("$", "")
                    data = tmp.split(",")

                    measureItem["data"] = tmp
                    measureItem["time"] = TimeUtil.getNewTimeByLong()

                    if len(data) < 5: continue
                    if len(data[0]) > 1: continue
                    # print("len : %d"%len(data[0]))

                    # print("%d, %d, %d, %d, %d"
                    #       % (
                    #           int(items[1]),
                    #           int(items[2]),
                    #           int(items[3]),
                    #           int(items[4]),
                    #           int(items[5])
                    #       )
                    #       )

                    # slope data
                    if self.slopeCount >= self.slopeInterval:
                        # print("slopeItems.append")
                        self.slopeCount = 1
                        self.slopeTimeCheckCount += 1
                        self.slopeWriteFile(self.slopeFile, measureItem, self.slopeItems)

                        if self.slopeTimeCheckCount >= SerialManager.slopeIntervalPerSec:
                            self.slopeTimeCheckCount = 0
                            if TimeUtil.checkAClock(SerialManager.slopeMeasureMin):
                                if self.slopeFile == None:
                                    print("file open")
                                    fileName = "slopeFile.csv"
                                    interval = format(1/SerialManager.slopeIntervalPerSec, ".2f")
                                    self.slopeFile = open("slopeFile.csv", 'w')
                                    self.slopeDiff = 0.0
                                    self.writeFileHeader(self.slopeFile, fileName, interval, True)
                                    self.slopeBufferDataWriteFile(self.slopeFile, self.slopeItems)
                                    # TODO: - file header 추가 및 버퍼 데이터 추가
                                    print("정시 측정 시작")
                            else:
                                if self.slopeFile != None:
                                    print("file close")
                                    self.slopeFile.close()
                                    self.slopeFile = None
                                    # TODO: - file close and upload
                                    print("정시 측정 종료")


                    else:
                        self.slopeCount += 1

                    while len(self.slopeItems) > self.slopeSaveCount:
                        self.slopeItems.pop(0)

                    # accel data
                    if self.accelCount >= self.accelInterval:
                        self.accelCount = 1
                        self.accelTimeCheckCount += 1
                        self.accelWriteFile(self.accelFile, measureItem, self.accelItems)

                        if int(data[2]) < self.abnormalData \
                                and not self.emergencyFlag:
                            self.emergencyFlag = True
                            print("지진 발생")

                        if self.emergencyFlag:
                            self.safetyCount += 1
                            # TODO: - file write

                            if self.safetyCount > self.accelSaveCount \
                                    and self.emergencyFlag:
                                print("지진 종료")
                                self.emergencyFlag = False
                                # TODO: - upload
                                self.safetyCount = 0

                        if self.requestFlag:
                            self.requestCount += 1
                            # TODO: - file write

                            if self.requestCount > self.accelSaveCount \
                                    and self.requestFlag:
                                print("지진 종료")
                                # self.uploadAccelMeasureItems()
                                self.emergencyFlag = False
                                # TODO: - upload
                                self.requestCount = 0

                        if self.accelTimeCheckCount >= SerialManager.accelIntervalPerSec:
                            if TimeUtil.checkAClock(SerialManager.accelMeasureMin):
                                if self.accelFile == None:
                                    print("file open")
                                    self.accelFile = open("accelFile.csv", 'w')
                                    self.accelDiff = 0.0
                                    fileName = "accelFile.csv"
                                    interval = format(1/SerialManager.accelIntervalPerSec, ".2f")
                                    self.writeFileHeader(self.accelFile, fileName, interval, False)
                                    self.accelBufferDataWriteFile(self.accelFile, self.accelItems)
                                    # TODO: - file header 추가 및 버퍼 데이터 추가
                                    print("정시 측정 시작")
                            else:
                                if self.accelFile != None:
                                    print("file close")
                                    self.accelFile.close()
                                    self.accelFile = None
                                    # TODO: - file close and upload
                                    print("정시 측정 종료")

                    else:
                        self.accelCount += 1

                    while len(self.accelItems) > self.accelSaveCount \
                            and not self.emergencyFlag:
                        self.accelItems.pop(0)

                # if len(self.items) >= 100:
                # copyItems = copy.deepcopy(self.items)
                # api.addMeasureItems(copyItems)
                # self.items.clear()

    # TODO: - measure을 서로 다르게해서 업로드할 것
    def uploadAccelMeasureItems(self):
        print("uploadAccelMeasureItems")
        copyItems = copy.deepcopy(self.accelItems)
        api.addMeasureItems(copyItems)
        self.accelItems.clear()

    def uploadSlopeMeasureItems(self):
        print("uploadSlopeMeasureItems")
        copyItems = copy.deepcopy(self.slopeItems)
        api.addMeasureItems(copyItems)
        self.slopeItems.clear()

    def slopeWriteFile(self, file, nextItem, items):

        if file == None:
            items.append(nextItem)
            return

        time = nextItem["time"]
        data = nextItem["data"]
        lenItems = len(items)

        if lenItems > 0:
            self.slopeDiff += float(nextItem["time"] - items[lenItems - 1]["time"]) / 1000.0

        items.append(nextItem)
        self.writeFile(file, time, self.slopeDiff, data)

    def accelWriteFile(self, file, nextItem, items):
        if file == None:
            items.append(nextItem)
            return

        time = nextItem["time"]
        data = nextItem["data"]
        lenItems = len(items)

        if lenItems > 0:
            self.accelDiff += float(nextItem["time"] - items[lenItems - 1]["time"]) / 1000.0

        items.append(nextItem)
        self.writeFile(file, time, self.accelDiff, data)

    def writeFile(self, file, time, diff, data):
        self.stringList.append(str(TimeUtil.longToDate(time)))
        self.stringList.append(" , ")
        self.stringList.append(format(diff, ".2f"))
        self.stringList.append(data)

        writeString = ''.join(self.stringList)
        writeString = writeString.replace('\n', '')
        self.stringList.clear()
        print(writeString)
        file.write(writeString)

    def writeFileHeader(self, file, fileName, interval, isStatic):
        headerList = []
        headerList.append("Datafile Ver 1.0, ")
        if isStatic:
            headerList.append("static , ")
        else:
            headerList.append("dynamic , ")

        headerList.append(str(TimeUtil.getNewDate()))
        headerList.append("\n")

        headerList.append("Date , ")
        headerList.append(str(TimeUtil.getNewDate()))
        headerList.append("\n")

        headerList.append("Filename , ")
        headerList.append(fileName)
        headerList.append("\n")

        headerList.append("Measure Interval , ")
        # headerList.append(format(1/headerList.append("Measure Interval , "), ".2f"))
        headerList.append(interval)
        headerList.append("\n")

        headerList.append("Channel Number , 5\n")
        headerList.append("DateTime , Elasped_Time(sec) , CH1 , CH2, CH3 , CH4 , CH5\n")
        writeString = ''.join(headerList)
        print(writeString)
        file.write(writeString)

    def slopeBufferDataWriteFile(self, file, items):
        for idx in range(0, len(items)):

            time = items[idx]["time"]
            data = items[idx]["data"]

            if idx > 0:
                self.slopeDiff += float(time - items[idx - 1]["time"]) / 1000.0
            self.writeFile(file, time, self.slopeDiff, data)

    def accelBufferDataWriteFile(self, file, items):
        for idx in range(0, len(items)):

            time = items[idx]["time"]
            data = items[idx]["data"]

            if idx > 0:
                self.accelDiff += float(time - items[idx - 1]["time"]) / 1000.0
            self.writeFile(file, time, self.accelDiff, data)




    def end(self):
        self.exitMeasureThread = False

        if self.serial is None:
            self.serial = serial.Serial(SerialManager.port, SerialManager.baud, timeout=0)

        self.serial.write(b"*T$")
        self.serial.close()
        self.serial = None


# Test Code
if __name__ == "__main__":
    manager = SerialManager()
    manager.start()
    # manager.end()
