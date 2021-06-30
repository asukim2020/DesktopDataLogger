import json

import serial
import threading
from python.serial.RequestApi import RequestApi as api

from python.serial.TimeUtil import TimeUtil


class SerialManager:
    # port = "/dev/ttyS0"
    port = "/dev/ttyAMA0"
    # port = "COM1"
    baud = 38400
    saveBufferTime = 30

    instance = None

    abnormalData = 0

    accelMeasureHour = 1
    slopeMeasureHour = 1

    accelMeasureMin = 10
    slopeMeasureMin = 10

    accelIntervalPerSec = 100
    slopeIntervalPerSec = 1

    def __init__(self):
        super().__init__()

        # 객체 변수 선언
        self.serial = None
        self.line = []
        self.exitMeasureThread = False

        self.triggerFlag = False
        self.triggerCount = 0
        self.triggerFile = None
        self.triggerDiff = 0.0

        self.slopeRequestFile = None
        self.slopeRequestCount = 0
        self.slopeRequestDiff = 0.0
        self.slopeRequestCount = 0
        self.slopeRequestSec = 10

        self.accelRequestFile = None
        self.accelRequestCount = 0
        self.accelRequestDiff = 0.0
        self.accelRequestCount = 0
        self.accelRequestSec = 10

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
                        self.slopeRequestWriteFile(self.slopeRequestFile, self.slopeItems)

                        if self.slopeTimeCheckCount >= SerialManager.slopeIntervalPerSec:
                            self.slopeTimeCheckCount = 0
                            if TimeUtil.checkAClock(SerialManager.slopeMeasureHour, SerialManager.slopeMeasureMin):
                                if self.slopeFile == None:
                                    api.setCompany()
                                    print("file open")
                                    fileName = "accel_request.csv"
                                    interval = format(1/SerialManager.slopeIntervalPerSec, ".2f")
                                    self.slopeFile = open("accel_request.csv", 'w')
                                    self.slopeDiff = 0.0
                                    self.writeFileHeader(self.slopeFile, fileName, interval, True)
                                    print("정시 측정 시작")
                            else:
                                if self.slopeFile != None:
                                    print("file close")
                                    self.slopeFile.close()
                                    self.slopeFile = None
                                    print("정시 측정 종료")
                                    api.slopeFileUpload()

                        # request
                        if self.slopeRequestFile != None:
                            if self.slopeRequestCount >= (self.slopeRequestSec * SerialManager.slopeIntervalPerSec):
                                self.closeSlopeRequestFile()

                    else:
                        self.slopeCount += 1

                    while len(self.slopeItems) > self.slopeSaveCount:
                        self.slopeItems.pop(0)

                    # accel data
                    if self.accelCount >= self.accelInterval:
                        self.accelCount = 1
                        self.accelTimeCheckCount += 1
                        self.accelWriteFile(self.accelFile, measureItem, self.accelItems)
                        self.accelRequestWriteFile(self.accelRequestFile, self.accelItems)

                        # trigger check
                        if int(data[2]) < SerialManager.abnormalData \
                                and not self.triggerFlag:
                            self.triggerFlag = True
                            print("지진 발생")

                            if self.triggerFile == None:
                                print("file open")
                                self.triggerFile = open("trigger.csv", 'w')
                                self.triggerDiff = 0.0
                                fileName = "trigger.csv"
                                interval = format(1 / SerialManager.accelIntervalPerSec, ".2f")
                                self.writeFileHeader(self.triggerFile, fileName, interval, False)
                                self.triggerBufferDataWriteFile(self.triggerFile, self.accelItems)

                        # trigger save
                        if self.triggerFlag:
                            self.triggerCount += 1
                            self.triggerWriteFile(self.triggerFile, self.accelItems)

                            if self.triggerCount > self.accelSaveCount \
                                    and self.triggerFlag:
                                print("지진 종료")
                                self.triggerFlag = False
                                self.triggerCount = 0

                                if self.triggerFile != None:
                                    print("file close")
                                    self.triggerFile.close()
                                    self.triggerFile = None
                                    api.triggerFileUpload()

                        # request
                        if self.accelRequestFile != None:
                            if self.accelRequestCount >= (self.accelRequestSec * SerialManager.accelIntervalPerSec):
                                self.closeAccelRequestFile()

                        if self.accelTimeCheckCount >= SerialManager.accelIntervalPerSec:
                            if TimeUtil.checkAClock(SerialManager.accelMeasureHour, SerialManager.accelMeasureMin):
                                if self.accelFile == None:
                                    print("file open")
                                    self.accelFile = open("accel.csv", 'w')
                                    self.accelDiff = 0.0
                                    fileName = "accel.csv"
                                    interval = format(1/SerialManager.accelIntervalPerSec, ".2f")
                                    self.writeFileHeader(self.accelFile, fileName, interval, False)
                                    print("정시 측정 시작")
                            else:
                                if self.accelFile != None:
                                    print("file close")
                                    self.accelFile.close()
                                    self.accelFile = None
                                    api.accelFileUpload()
                                    print("정시 측정 종료")

                    else:
                        self.accelCount += 1

                    while len(self.accelItems) > self.accelSaveCount \
                            and not self.triggerFlag:
                        self.accelItems.pop(0)

                # if len(self.items) >= 100:
                # copyItems = copy.deepcopy(self.items)
                # api.addMeasureItems(copyItems)
                # self.items.clear()

    # TODO: - measure을 서로 다르게해서 업로드할 것
    # def uploadAccelMeasureItems(self):
    #     print("uploadAccelMeasureItems")
    #     copyItems = copy.deepcopy(self.accelItems)
    #     api.addMeasureItems(copyItems)
    #     self.accelItems.clear()
    #
    # def uploadSlopeMeasureItems(self):
    #     print("uploadSlopeMeasureItems")
    #     copyItems = copy.deepcopy(self.slopeItems)
    #     api.addMeasureItems(copyItems)
    #     self.slopeItems.clear()

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

    def triggerWriteFile(self, file, items):
        if file == None:
            return

        lenItem = len(items)

        if lenItem < 2: return

        time = items[lenItem - 1]["time"]
        data = items[lenItem - 1]["data"]
        lenItems = len(items)

        if lenItems > 0:
            self.triggerDiff += float(items[lenItem - 1]["time"] - items[lenItems - 2]["time"]) / 1000.0

        self.writeFile(file, time, self.triggerDiff, data)

    def slopeRequestWriteFile(self, file, items):
        if file == None:
            return

        lenItem = len(items)

        if lenItem < 2: return

        time = items[lenItem - 1]["time"]
        data = items[lenItem - 1]["data"]
        lenItems = len(items)

        if lenItems > 0:
            self.slopeRequestDiff += float(items[lenItem - 1]["time"] - items[lenItems - 2]["time"]) / 1000.0

        self.writeFile(file, time, self.slopeRequestDiff, data)
        self.slopeRequestCount +=1

    def accelRequestWriteFile(self, file, items):
        if file == None:
            return

        lenItem = len(items)

        if lenItem < 2: return

        time = items[lenItem - 1]["time"]
        data = items[lenItem - 1]["data"]
        lenItems = len(items)

        if lenItems > 0:
            self.accelRequestDiff += float(items[lenItem - 1]["time"] - items[lenItems - 2]["time"]) / 1000.0

        self.writeFile(file, time, self.accelRequestDiff, data)
        self.accelRequestCount += 1

    def writeFile(self, file, time, diff, data):
        try:
            self.stringList.append(str(TimeUtil.longToDate(time)))
            self.stringList.append(" , ")
            self.stringList.append(format(diff, ".2f"))
            self.stringList.append(data)

            writeString = ''.join(self.stringList)
            writeString = writeString.replace('\n', '')
            self.stringList.clear()
            print(writeString)
            file.write(writeString)
        except Exception as e:
            print(e)

    def writeFileHeader(self, file, fileName, interval, isStatic):
        try:
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
        except Exception as e:
            print(e)

    def createSlopeRequestFile(self):
        if self.slopeRequestFile == None:
            self.slopeDiff = 0
            self.slopeRequestCount = 0

            fileName = 'sloperequest.csv'
            self.slopeRequestFile = open(fileName, 'w')
            interval = format(1 / SerialManager.slopeIntervalPerSec, ".2f")
            self.writeFileHeader(self.slopeRequestFile, fileName, interval, True)

    def createAccelRequestFile(self):
        if self.accelRequestFile == None:
            self.accelDiff = 0
            self.accelRequestCount = 0

            fileName = 'accelrequest.csv'
            self.accelRequestFile = open(fileName, 'w')
            interval = format(1 / SerialManager.accelIntervalPerSec, ".2f")
            self.writeFileHeader(self.accelRequestFile, fileName, interval, False)

    def closeSlopeRequestFile(self):
        if self.slopeRequestFile != None:
            self.slopeRequestFile.close()
            self.slopeRequestFile = None
            api.slopeRequestFileUpload()

    def closeAccelRequestFile(self):
        if self.accelRequestFile != None:
            self.accelRequestFile.close()
            self.accelRequestFile = None
            api.accelRequestFileUpload()

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

    def triggerBufferDataWriteFile(self, file, items):
        for idx in range(0, len(items)):

            time = items[idx]["time"]
            data = items[idx]["data"]

            if idx > 0:
                self.triggerDiff += float(time - items[idx - 1]["time"]) / 1000.0
            self.writeFile(file, time, self.triggerDiff, data)

    # def requestBufferDataWriteFile(self, file, items):
    #     for idx in range(0, len(items)):
    #
    #         time = items[idx]["time"]
    #         data = items[idx]["data"]
    #
    #         if idx > 0:
    #             self.requestDiff += float(time - items[idx - 1]["time"]) / 1000.0
    #         self.writeFile(file, time, self.requestDiff, data)

    @classmethod
    def setSettingData(
            cls,
            abnormalData,
            accelMeasureHour,
            slopeMeasureHour,
            accelMeasureMin,
            slopeMeasureMin,
            accelIntervalPerSec,
            slopeIntervalPerSec
    ):
        SerialManager.abnormalData = abnormalData

        SerialManager.accelMeasureHour = accelMeasureHour
        SerialManager.slopeMeasureHour = slopeMeasureHour

        SerialManager.accelMeasureMin = accelMeasureMin
        SerialManager.slopeMeasureMin = slopeMeasureMin

        SerialManager.accelIntervalPerSec = accelIntervalPerSec
        SerialManager.slopeIntervalPerSec = slopeIntervalPerSec

    @classmethod
    def saveSettingData(self):
        try:
            dic = {}
            dic["abnormalData"] = SerialManager.abnormalData

            dic["accelMeasureHour"] = SerialManager.accelMeasureHour
            dic["slopeMeasureHour"] = SerialManager.slopeMeasureHour

            dic["accelMeasureMin"] = SerialManager.accelMeasureMin
            dic["slopeMeasureMin"] = SerialManager.slopeMeasureMin

            dic["accelIntervalPerSec"] = SerialManager.accelIntervalPerSec
            dic["slopeIntervalPerSec"] = SerialManager.slopeIntervalPerSec

            settingFile = open("setting.txt", 'w')
            jsonString = json.dumps(dic)
            settingFile.write(jsonString)
            settingFile.close()

            print("abnormalData: %d" % SerialManager.abnormalData)

            print("accelMeasureHour: %d" % SerialManager.accelMeasureHour)
            print("slopeMeasureHour: %d" % SerialManager.slopeMeasureHour)

            print("accelMeasureMin: %d" % SerialManager.accelMeasureMin)
            print("slopeMeasureMin: %d" % SerialManager.slopeMeasureMin)

            print("accelIntervalPerSec: %d" % SerialManager.accelIntervalPerSec)
            print("slopeIntervalPerSec: %d" % SerialManager.slopeIntervalPerSec)
        except Exception as e:
            print(e)

    @classmethod
    def getSettingData(self):
        try:
            settingFile = open("setting.txt", 'r')
            jsonStringList = []
            while True:
                line = settingFile.readline()
                if not line: break
                jsonStringList.append(line)

            jsonString = ''.join(jsonStringList)

            dic = json.loads(jsonString)

            SerialManager.abnormalData = dic["abnormalData"]

            SerialManager.accelMeasureHour = dic["accelMeasureHour"]
            SerialManager.slopeMeasureHour = dic["slopeMeasureHour"]

            SerialManager.accelMeasureMin = dic["accelMeasureMin"]
            SerialManager.slopeMeasureMin = dic["slopeMeasureMin"]

            SerialManager.accelIntervalPerSec = dic["accelIntervalPerSec"]
            SerialManager.slopeIntervalPerSec = dic["slopeIntervalPerSec"]

            settingFile.close()

            print("abnormalData: %d"%SerialManager.abnormalData)

            print("accelMeasureHour: %d" % SerialManager.accelMeasureHour)
            print("slopeMeasureHour: %d" % SerialManager.slopeMeasureHour)

            print("accelMeasureMin: %d" % SerialManager.accelMeasureMin)
            print("slopeMeasureMin: %d" % SerialManager.slopeMeasureMin)

            print("accelIntervalPerSec: %d" % SerialManager.accelIntervalPerSec)
            print("slopeIntervalPerSec: %d" % SerialManager.slopeIntervalPerSec)
        except Exception as e:
            print(e)



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
