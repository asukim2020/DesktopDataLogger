import json
import math

import serial
import threading

from python.serial.RequestApi import RequestApi as api

from python.serial.TimeUtil import TimeUtil


class SerialManager:
    # port = "/dev/ttyS0"
    # port = "/dev/ttyAMA0"
    port = "COM1"
    baud = 38400
    saveBufferTime = 30

    instance = None

    abnormalXMin = 0
    abnormalXMax = 30000

    abnormalYMin = 0
    abnormalYMax = 30000

    abnormalZMin = 0
    abnormalZMax = 30000

    accelMeasureHour = 1
    slopeMeasureHour = 1

    accelMeasureMin = 5
    slopeMeasureMin = 5

    accelIntervalPerSec = 100
    slopeIntervalPerSec = 1

    def __init__(self):
        super().__init__()

        # 객체 변수 선언
        self.serial = None
        self.line = []
        self.exitMeasureThread = False

        self.triggerFlag = False
        self.triggerOccurCount = 0
        self.triggerCount = 0
        self.triggerFile = None
        self.triggerDiff = 0.0

        self.slopeRequestFile = None
        self.slopeRequestCount = 0
        self.slopeRequestDiff = 0.0
        self.slopeRequestSec = 10

        self.accelRequestFile = None
        self.accelRequestCount = 0
        self.accelRequestDiff = 0.0
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
        self.slopeSumX = 0
        self.slopeSumY = 0

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

                try:
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
                        #           int(data[1]),
                        #           int(data[2]),
                        #           int(data[3]),
                        #           int(data[4]),
                        #           int(data[5])
                        #       )
                        #       )

                        # slope data
                        self.slopeSumX += int(data[4])
                        self.slopeSumY += int(data[5])
                        if self.slopeCount >= self.slopeInterval:
                            avgX = self.slopeSumX / self.slopeInterval
                            avgY = self.slopeSumY / self.slopeInterval
                            self.slopeSumX = 0
                            self.slopeSumY = 0

                            item = {}
                            item["data"] = ' %d , %d\r\n' % (avgX, avgY)
                            item["time"] = measureItem["time"]

                            self.slopeCount = 1
                            self.slopeTimeCheckCount += 1
                            self.slopeWriteFile(self.slopeFile, item, self.slopeItems,
                                                self.slopeTimeCheckCount >= SerialManager.slopeIntervalPerSec)
                            self.slopeRequestWriteFile(self.slopeRequestFile, self.slopeItems,
                                                       self.slopeTimeCheckCount >= SerialManager.slopeIntervalPerSec)

                            if self.slopeTimeCheckCount >= SerialManager.slopeIntervalPerSec:
                                self.slopeTimeCheckCount = 0
                                if TimeUtil.checkAClock(SerialManager.slopeMeasureHour, SerialManager.slopeMeasureMin):
                                    if self.slopeFile == None:
                                        api.setCompany()
                                        api.deleteFile()
                                        fileName = "slope.csv"
                                        interval = format(1 / SerialManager.slopeIntervalPerSec, ".2f")
                                        self.slopeFile = open(fileName, 'w')
                                        self.slopeDiff = 0.0
                                        self.writeFileHeader(self.slopeFile, fileName, interval, True, 2)
                                        print("[경사센서 정시측정] 시작")
                                else:
                                    if self.slopeFile != None:
                                        self.slopeFile.close()
                                        self.slopeFile = None
                                        print("[경사센서 정시측정] 종료")
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
                            item = {}
                            item["data"] = '%s,%s,%s\r\n' % (data[1], data[2], data[3])
                            item["time"] = measureItem["time"]


                            self.accelCount = 1
                            self.accelTimeCheckCount += 1
                            self.accelWriteFile(self.accelFile, item, self.accelItems,
                                                self.accelTimeCheckCount >= SerialManager.accelIntervalPerSec)
                            self.accelRequestWriteFile(self.accelRequestFile, self.accelItems,
                                                       self.accelTimeCheckCount >= SerialManager.accelIntervalPerSec)

                            # trigger check
                            x = int(data[1])
                            y = int(data[2])
                            z = int(data[3])
                            # print('x: %d, y: %d, z: %d'%(x, y, z))
                            if \
                                    (not(SerialManager.abnormalXMin <= x <= SerialManager.abnormalXMax)
                                     or not(SerialManager.abnormalYMin <= y <= SerialManager.abnormalYMax)
                                     or not(SerialManager.abnormalZMin <= z <= SerialManager.abnormalZMax)) \
                                            and not self.triggerFlag:

                                self.triggerFlag = True
                                print("[트리거 발생]")
                                print('x: %d, y: %d, z: %d' % (x, y, z))

                                if self.triggerFile == None:
                                    fileName = "trigger.csv"
                                    self.triggerFile = open(fileName, 'w')
                                    self.triggerDiff = 0.0
                                    interval = format(1 / SerialManager.accelIntervalPerSec, ".2f")
                                    self.writeFileHeader(self.triggerFile, fileName, interval, False, 3)
                                    self.triggerBufferDataWriteFile(self.triggerFile, self.accelItems)

                            # trigger save
                            if self.triggerFlag:
                                self.triggerCount += 1
                                self.triggerWriteFile(self.triggerFile, self.accelItems, self.accelTimeCheckCount >= SerialManager.accelIntervalPerSec)

                                if self.triggerCount > self.accelSaveCount \
                                        and self.triggerFlag:
                                    print("[트리거 측정 종료]")
                                    self.triggerFlag = False
                                    self.triggerCount = 0

                                    if self.triggerFile != None:
                                        self.triggerFile.close()
                                        self.triggerFile = None
                                        api.triggerFileUpload()

                            # request
                            if self.accelRequestFile != None:
                                if self.accelRequestCount >= (self.accelRequestSec * SerialManager.accelIntervalPerSec):
                                    self.closeAccelRequestFile()

                            if self.accelTimeCheckCount >= SerialManager.accelIntervalPerSec:
                                self.accelTimeCheckCount = 0
                                if TimeUtil.checkAClock(SerialManager.accelMeasureHour, SerialManager.accelMeasureMin):
                                    if self.accelFile == None:
                                        fileName = "accel.csv"
                                        self.accelFile = open(fileName, 'w')
                                        self.accelDiff = 0.0
                                        interval = format(1 / SerialManager.accelIntervalPerSec, ".2f")
                                        self.writeFileHeader(self.accelFile, fileName, interval, False, 3)
                                        print("[가속도센서 정시측정] 시작")
                                else:
                                    if self.accelFile != None:
                                        self.accelFile.close()
                                        self.accelFile = None
                                        print("[가속도센서 정시측정] 종료")
                                        api.accelFileUpload()

                        else:
                            self.accelCount += 1

                        while len(self.accelItems) > self.accelSaveCount \
                                and not self.triggerFlag:
                            self.accelItems.pop(0)
                except Exception as e:
                    print(e)


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

    def slopeWriteFile(self, file, nextItem, items, isPrint=False):
        if file == None:
            items.append(nextItem)
            return

        time = nextItem["time"]
        data = nextItem["data"]
        lenItems = len(items)

        if lenItems > 0:
            self.slopeDiff += 1 / SerialManager.slopeIntervalPerSec

        items.append(nextItem)
        self.writeFile(file, time, self.slopeDiff, data, isPrint)

    def accelWriteFile(self, file, nextItem, items, isPrint=False):
        if file == None:
            items.append(nextItem)
            return

        time = nextItem["time"]
        data = nextItem["data"]
        lenItems = len(items)

        if lenItems > 0:
            self.accelDiff += 1 / SerialManager.accelIntervalPerSec

        items.append(nextItem)
        self.writeFile(file, time, self.accelDiff, data, isPrint)

    def triggerWriteFile(self, file, items, isPrint=False):
        if file == None:
            return

        lenItem = len(items)

        if lenItem < 2: return

        time = items[lenItem - 1]["time"]
        data = items[lenItem - 1]["data"]
        lenItems = len(items)

        if lenItems > 0:
            self.triggerDiff += 1 / SerialManager.accelIntervalPerSec

        self.writeFile(file, time, self.triggerDiff, data, isPrint)

    def slopeRequestWriteFile(self, file, items, isPrint=False):
        if file == None:
            return

        lenItem = len(items)

        if lenItem < 2: return

        time = items[lenItem - 1]["time"]
        data = items[lenItem - 1]["data"]
        lenItems = len(items)

        if lenItems > 0:
            self.slopeRequestDiff += 1 / SerialManager.slopeIntervalPerSec

        self.writeFile(file, time, self.slopeRequestDiff, data, isPrint)
        self.slopeRequestCount += 1

    def accelRequestWriteFile(self, file, items, isPrint=False):
        if file == None:
            return

        lenItem = len(items)

        if lenItem < 2: return

        time = items[lenItem - 1]["time"]
        data = items[lenItem - 1]["data"]
        lenItems = len(items)

        if lenItems > 0:
            self.accelRequestDiff += 1 / SerialManager.accelIntervalPerSec

        self.writeFile(file, time, self.accelRequestDiff, data, isPrint)
        self.accelRequestCount += 1

    def writeFile(self, file, time, diff, data, isPrint=False):
        try:
            self.stringList.append(str(TimeUtil.longToDate(time)))
            self.stringList.append(" , ")
            self.stringList.append(format(diff, ".2f"))
            self.stringList.append(" ,")
            self.stringList.append(data)

            writeString = ''.join(self.stringList)
            writeString = writeString.replace('\n', '')
            self.stringList.clear()
            diff = round(diff, 2)
            if diff % 1.0 == 0:
                if file == self.slopeFile:
                    print('[경사센서 정시측정]: ' + writeString)
                elif file == self.accelFile:
                    print('[가속도센서 정시측정]: ' + writeString)
                elif file == self.triggerFile:
                    print('[트리거 측정]: ' + writeString)
                elif file == self.slopeRequestFile:
                    print('[경사센서 요청측정]: ' + writeString)
                elif file == self.accelRequestFile:
                    print('[가속도센서 요청측정]: ' + writeString)

            file.write(writeString)
        except Exception as e:
            print(e)

    def writeFileHeader(self, file, fileName, interval, isStatic, count):
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

            if count == 2:
                headerList.append("Channel Number , 2\n")
                headerList.append("DateTime , Elasped_Time(sec) , CH1 , CH2\n")
            elif count == 3:
                headerList.append("Channel Number , 3\n")
                headerList.append("DateTime , Elasped_Time(sec) , CH1 , CH2, CH3\n")
            writeString = ''.join(headerList)
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
            self.writeFileHeader(self.slopeRequestFile, fileName, interval, True, 2)

    def createAccelRequestFile(self):
        if self.accelRequestFile == None:
            self.accelDiff = 0
            self.accelRequestCount = 0

            fileName = 'accelrequest.csv'
            self.accelRequestFile = open(fileName, 'w')
            interval = format(1 / SerialManager.accelIntervalPerSec, ".2f")
            self.writeFileHeader(self.accelRequestFile, fileName, interval, False, 3)

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

    def triggerBufferDataWriteFile(self, file, items):
        for idx in range(0, len(items)):

            time = items[idx]["time"]
            data = items[idx]["data"]

            self.triggerDiff += 1 / SerialManager.accelIntervalPerSec
            self.writeFile(file, time, self.triggerDiff, data)


    @classmethod
    def getStandardAClock(cls):
        return SerialManager.standardAClock

    @classmethod
    def getStandardAMin(cls):
        return SerialManager.standardAMin

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
