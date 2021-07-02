import json
import threading
import time

import requests


class MeasureSetting:
    lastStringRequestTime = 0
    url = 'http://3.37.113.193:8080'
    # url = 'http://localhost:8080'

    def start(self):
        thread = threading.Thread(target=self.repeatSetting)
        thread.start()

    def repeatSetting(self):
        while True:
            self.getSetting()

    def getSetting(cls):
        time.sleep(5)
        print('getSetting')
        from python.serial.SerialManager import SerialManager
        from python.serial.TimeUtil import TimeUtil
        try:
            response = requests.get(cls.url + '/measure/get/setting')
            jstr = response.text
            print(jstr)
            dic = json.loads(jstr)

            if (MeasureSetting.lastStringRequestTime >= dic['time']):
                return

            MeasureSetting.lastStringRequestTime = dic['time']
            print('lastTime: %d'%MeasureSetting.lastStringRequestTime)
            accelList = dic['accel'].split('_')
            if len(accelList) == 3:
                SerialManager.accelMeasureHour = int(accelList[0])
                SerialManager.accelMeasureMin = int(accelList[1])
                SerialManager.accelIntervalPerSec = int(accelList[2])
                instance = SerialManager.instance
                if instance == None: return
                instance.accelInterval = 100 / SerialManager.accelIntervalPerSec
                instance.accelSaveCount = SerialManager.saveBufferTime * SerialManager.accelIntervalPerSec
                print('accel: %s'% dic['accel'])

            slopeList = dic['slope'].split('_')
            if len(slopeList) == 3:
                SerialManager.slopeMeasureHour = int(slopeList[0])
                SerialManager.slopeMeasureMin = int(slopeList[1])
                SerialManager.slopeIntervalPerSec = int(slopeList[2])
                instance = SerialManager.instance
                if instance == None: return
                instance.slopeInterval = 100 / SerialManager.slopeIntervalPerSec
                instance.slopeSaveCount = SerialManager.saveBufferTime * SerialManager.slopeIntervalPerSec
                print('slope: %s'% dic['slope'])

            triggerList = dic['triggerLevel'].split('_')
            if len(triggerList) == 2:
                SerialManager.abnormalDataMin = int(triggerList[0])
                SerialManager.abnormalDataMax = int(triggerList[1])
                print('triggerLevel: %s'% dic['triggerLevel'])

            timeList = dic['standardTime'].split('_')
            if len(timeList) == 2:
                TimeUtil.standardHour = int(timeList[0])
                TimeUtil.standardMin = int(timeList[1])
                print('standardTime: %s'% dic['standardTime'])

            if MeasureSetting.lastStringRequestTime == 0:
                return

            request = dic['request']
            if '*RS' in request:
                instance = SerialManager.instance
                if instance == None: return
                instance.createSlopeRequestFile()
                request = request.replace('*RS', '')
                request = request.replace('$', '')
                request = request.replace('_', '')
                try:
                    sec = int(request)
                    instance.slopeRequestSec = sec
                except Exception as e:
                    print(e)

                print('createSlopeRequestFile()')
            elif '*RA' in request:
                instance = SerialManager.instance
                if instance == None: return
                instance.createAccelRequestFile()
                request = request.replace('*RA', '')
                request = request.replace('$', '')
                request = request.replace('_', '')
                try:
                    sec = int(request)
                    instance.accelRequestSec = sec
                except Exception as e:
                    print(e)

                print('createAccelRequestFile()')


        except requests.exceptions.HTTPError as errh:
            print(errh)
        except requests.exceptions.ConnectionError as errc:
            print(errc)
        except requests.exceptions.Timeout as errt:
            print(errt)
        except requests.exceptions.RequestException as err:
            print(err)
        except Exception as e:
            print(e)