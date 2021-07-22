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
        from python.serial.SerialManager import SerialManager
        from python.serial.TimeUtil import TimeUtil
        try:
            response = requests.get(cls.url + '/measure/get/setting')
            jstr = response.text
            dic = json.loads(jstr)

            if (MeasureSetting.lastStringRequestTime >= dic['time']):
                return

            instance = SerialManager.instance
            if instance == None: return

            print('[측정 설정 반영]')
            accelList = dic['accel'].split('_')
            if len(accelList) == 3:
                SerialManager.accelMeasureHour = int(accelList[0])
                SerialManager.accelMeasureMin = int(accelList[1])
                SerialManager.accelIntervalPerSec = int(accelList[2])
                instance.accelInterval = 100 / SerialManager.accelIntervalPerSec
                instance.accelSaveCount = SerialManager.saveBufferTime * SerialManager.accelIntervalPerSec
                print('[가속도센서] 설정: %d시간마다 %d분동안 초당%d개 측정'%(int(accelList[0]), int(accelList[1]), int(accelList[2])))

            slopeList = dic['slope'].split('_')
            if len(slopeList) == 3:
                SerialManager.slopeMeasureHour = int(slopeList[0])
                SerialManager.slopeMeasureMin = int(slopeList[1])
                SerialManager.slopeIntervalPerSec = int(slopeList[2])
                instance.slopeInterval = 100 / SerialManager.slopeIntervalPerSec
                instance.slopeSaveCount = SerialManager.saveBufferTime * SerialManager.slopeIntervalPerSec
                print('[경사센서] 설정: %d시간마다 %d분동안 초당%d개 측정'%(int(slopeList[0]), int(slopeList[1]), int(slopeList[2])))

            triggerList = dic['triggerLevel'].split('_')
            if len(triggerList) == 6:
                SerialManager.abnormalXMin = int(triggerList[0])
                SerialManager.abnormalXMax = int(triggerList[1])
                SerialManager.abnormalYMin = int(triggerList[2])
                SerialManager.abnormalYMax = int(triggerList[3])
                SerialManager.abnormalZMin = int(triggerList[4])
                SerialManager.abnormalZMax = int(triggerList[5])
                print('[트리거 레벨] 설정: %d < x < %d, %d < y < %d, %d < z < %d' %(int(triggerList[0]), int(triggerList[1]), int(triggerList[2]), int(triggerList[3]), int(triggerList[4]), int(triggerList[5])))

            elif len(triggerList) == 7:
                SerialManager.abnormalXMin = int(triggerList[0])
                SerialManager.abnormalXMax = int(triggerList[1])
                SerialManager.abnormalYMin = int(triggerList[2])
                SerialManager.abnormalYMax = int(triggerList[3])
                SerialManager.abnormalZMin = int(triggerList[4])
                SerialManager.abnormalZMax = int(triggerList[5])
                SerialManager.saveBufferTime = int(triggerList[6])

                instance.accelSaveCount = SerialManager.saveBufferTime * SerialManager.accelIntervalPerSec
                instance.slopeSaveCount = SerialManager.saveBufferTime * SerialManager.slopeIntervalPerSec

                print('[트리거 레벨] 설정: 간격: %d, %d < x < %d, %d < y < %d, %d < z < %d' %(int(triggerList[6]), int(triggerList[0]), int(triggerList[1]), int(triggerList[2]), int(triggerList[3]), int(triggerList[4]), int(triggerList[5])))

            timeList = dic['standardTime'].split('_')
            if len(timeList) == 2:
                TimeUtil.standardHour = int(timeList[0])
                TimeUtil.standardMin = int(timeList[1])
                print('[기준시] 설정: %d시 %d분을 기준으로 측정 시작'%(int(timeList[0]), int(timeList[1])))

            if MeasureSetting.lastStringRequestTime == 0:
                MeasureSetting.lastStringRequestTime = dic['time']
                print('[측정 설정 반영 종료]')
                return

            request = dic['request']
            if '*RS' in request:
                instance.createSlopeRequestFile()
                request = request.replace('*RS', '')
                request = request.replace('$', '')
                request = request.replace('_', '')
                try:
                    sec = int(request)
                    instance.slopeRequestSec = sec
                except Exception as e:
                    print(e)

                print('[경사센서 요청측정]: %d초 측정'%int(request))
            elif '*RA' in request:
                instance.createAccelRequestFile()
                request = request.replace('*RA', '')
                request = request.replace('$', '')
                request = request.replace('_', '')
                try:
                    sec = int(request)
                    instance.accelRequestSec = sec
                except Exception as e:
                    print(e)

                print('[가속도센서 요청측정]: %d초 측정'%int(request))

            MeasureSetting.lastStringRequestTime = dic['time']

            print('[측정 설정 반영 종료]')

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