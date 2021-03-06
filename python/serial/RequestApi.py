from io import StringIO

import requests
import json

from python.serial.TimeUtil import TimeUtil


class RequestApi:
    url = 'http://3.37.113.193:8080'
    # url = 'http://localhost:8080'

    def __init__(self):
        super().__init__()

        # self.url = 'http://3.37.113.193:8080/'
        # self.url = 'http://localhost:8080'
        # self.url = 'http://211.184.136.231:8080'

    @classmethod
    def setCompany(cls):
        try:
            ip = requests.get('https://api.ipify.org')

            query = {
                'name': 'NGI',
                'ip': ip.text
            }
            response = requests.post(cls.url + '/measure/post/company', params=query)
            # print(response.text)
        except requests.exceptions.HTTPError as errh:
            print(errh)
        except requests.exceptions.ConnectionError as errc:
            print(errc)
        except requests.exceptions.Timeout as errt:
            print(errt)
        except requests.exceptions.RequestException as err:
            print(err)

    @classmethod
    def findCompany(cls):
        try:
            ip = requests.get('https://api.ipify.org')

            query = {
                'name': 'NGI'
            }
            response = requests.get(cls.url + '/measure/get/company/name', params=query)
            # print(response.text)
        except requests.exceptions.HTTPError as errh:
            print(errh)
        except requests.exceptions.ConnectionError as errc:
            print(errc)
        except requests.exceptions.Timeout as errt:
            print(errt)
        except requests.exceptions.RequestException as err:
            print(err)


    @classmethod
    def start(cls):
        try:
            # mode -> "step" or "interval"
            query = {
                'id': 1,
                'name': '12345'
            }
            response = requests.post(cls.url + '/measure/post/start', params=query)

            jstr = response.text
            json_data = json.loads(jstr)
            id = json_data['measureId']
            print(id)
            print(json_data['name'])
            return id

        except requests.exceptions.HTTPError as errh:
            print(errh)
        except requests.exceptions.ConnectionError as errc:
            print(errc)
        except requests.exceptions.Timeout as errt:
            print(errt)
        except requests.exceptions.RequestException as err:
            print(err)

        return -1



    @classmethod
    def addMeasureItems(cls, items):
        id = 2
        # obj = []
        # for i in range(0, 3):
        #     dic = {}
        #     dic["data"] = "*+1234+1234+1234$"
        #     dic["time"] = 1623892415373 + (10000 * i)
        #     obj.append(dic)

        try:
            query = {'id': id}
            response = requests.post(cls.url + "/measure/post/items", params=query, json=items)
            print(response)
        except requests.exceptions.HTTPError as errh:
            print(errh)
        except requests.exceptions.ConnectionError as errc:
            print(errc)
        except requests.exceptions.Timeout as errt:
            print(errt)
        except requests.exceptions.RequestException as err:
            print(err)

        # print(response.text)

        # jstr = StringIO('['
        #                 '{"data": "*+1234+1234+1234$","time": 1623892395373},'
        #                 '{"data": "*+1234+1234+1234$","time": 1623892405373},'
        #                 '{"data": "*+1234+1234+1234$","time": 1623892415373}'
        #                 ']'
        #                 )

        # json_data = json.load(jstr)
        # query = {'id': id}
        # requests.post(self.url + "/measure/post/items", params=query, json=json_data)

    @classmethod
    def getMeasureItems(cls):
        try:
            query = {
                'id': 2,
                'startTime': 1624342645174,
                'endTime': 1624342655078,
                'afterId': 0
            }
            response = requests.get(cls.url + '/measure/get/items/time', params=query)
            print(response)
            jstr = response.text
            json_data = json.loads(jstr)
            print(json.dumps(json_data, indent=4))
        except requests.exceptions.HTTPError as errh:
            print(errh)
        except requests.exceptions.ConnectionError as errc:
            print(errc)
        except requests.exceptions.Timeout as errt:
            print(errt)
        except requests.exceptions.RequestException as err:
            print(err)

    @classmethod
    def setSensorSetting(cls):
        id = 2
        obj = []
        for i in range(0, 3):
            dic = {}
            dic["number"] = "%02d" % (i + 1)
            dic["on"] = True
            dic["type"] = "0"
            dic["ampGain"] = "0"
            dic["applyV"] = "0"
            dic["filter"] = "0"
            obj.append(dic)

        print(obj)
        query = {'id': id}
        response = requests.post(cls.url + "/measure/sensor/set/list", params=query, json=obj)
        print(response)
        print(response.text)

    @classmethod
    def getSensorItems(cls):
        query = {'id': 2}
        response = requests.get(cls.url + '/measure/sensor/get/list', params=query)

        jstr = response.text
        json_data = json.loads(jstr)
        print(json.dumps(json_data, indent=4))

        sendStringList = []
        for item in json_data:
            # ?????? ?????? ?????????
            sendStringList.append("*U")

            # ?????? ?????? 2??????
            sendStringList.append(item["number"])

            # on: 1, off: 0 1??????
            sendStringList.append("1")

            # ?????? ?????? 2??????
            sendStringList.append(item["type"])

            # ???????????? 1??????
            sendStringList.append(item["ampGain"])

            # ???????????? 1??????
            sendStringList.append(item["applyV"])

            # ?????? 1?????????
            sendStringList.append(item["filter"])

            # ?????? ??????
            sendStringList.append("$\n")

        sendStringList.append("*E$\n")
        sendStringList.append("*S$\n")

        sendString = ''.join(sendStringList)
        print(sendString)

    @classmethod
    def slopeFileUpload(cls):
        try:
            f = open('slope.csv', 'rb')
            files = {"file": f}
            resp = requests.post(cls.url + '/file/upload/slope', files=files)

            if resp.status_code == 200:
                print("[???????????? ????????????] ????????? ??????")
            else:
                print("[???????????? ????????????] ??????")

            f.close()
        except requests.exceptions.HTTPError as errh:
            print(errh)
        except requests.exceptions.ConnectionError as errc:
            print(errc)
        except requests.exceptions.Timeout as errt:
            print(errt)
        except requests.exceptions.RequestException as err:
            print(err)

    @classmethod
    def accelFileUpload(cls):
        try:
            f = open('accel.csv', 'rb')
            files = {"file": f}
            resp = requests.post(cls.url + '/file/upload/accel', files=files)

            if resp.status_code == 200:
                print("[??????????????? ????????????] ????????? ??????")
            else:
                print("[??????????????? ????????????] ??????")

            f.close()
        except requests.exceptions.HTTPError as errh:
            print(errh)
        except requests.exceptions.ConnectionError as errc:
            print(errc)
        except requests.exceptions.Timeout as errt:
            print(errt)
        except requests.exceptions.RequestException as err:
            print(err)

    @classmethod
    def triggerFileUpload(cls):
        try:
            f = open('trigger.csv', 'rb')
            files = {"file": f}
            resp = requests.post(cls.url + '/file/upload/trigger', files=files)

            if resp.status_code == 200:
                print("[????????? ??????] ????????? ??????")
            else:
                print("[????????? ??????] ????????? ??????")

            f.close()
        except requests.exceptions.HTTPError as errh:
            print(errh)
        except requests.exceptions.ConnectionError as errc:
            print(errc)
        except requests.exceptions.Timeout as errt:
            print(errt)
        except requests.exceptions.RequestException as err:
            print(err)

    @classmethod
    def slopeRequestFileUpload(cls):
        try:
            f = open('sloperequest.csv', 'rb')
            files = {"file": f}
            resp = requests.post(cls.url + '/file/upload/slope/request', files=files)

            if resp.status_code == 200:
                print("[???????????? ????????????] ????????? ??????")
            else:
                print("[???????????? ????????????] ????????? ??????")

            f.close()
        except requests.exceptions.HTTPError as errh:
            print(errh)
        except requests.exceptions.ConnectionError as errc:
            print(errc)
        except requests.exceptions.Timeout as errt:
            print(errt)
        except requests.exceptions.RequestException as err:
            print(err)

    @classmethod
    def accelRequestFileUpload(cls):
        try:
            f = open('accelrequest.csv', 'rb')
            files = {"file": f}
            resp = requests.post(cls.url + '/file/upload/accel/request', files=files)

            if resp.status_code == 200:
                print("[??????????????? ????????????] ????????? ??????")
            else:
                print("[??????????????? ????????????] ????????? ??????")

            f.close()
        except requests.exceptions.HTTPError as errh:
            print(errh)
        except requests.exceptions.ConnectionError as errc:
            print(errc)
        except requests.exceptions.Timeout as errt:
            print(errt)
        except requests.exceptions.RequestException as err:
            print(err)

    @classmethod
    def fileUpload(cls):
        try:
            f = open('C:/Users/Asu/Downloads/????????????2/015.csv', 'rb')

            files = {"file": f}

            resp = requests.post(cls.url + '/file/upload/slope', files=files)
            # resp = requests.post(cls.url + '/file/upload/accel', files=files)
            # resp = requests.post(cls.url + '/file/upload/trigger', files=files)
            # resp = requests.post(cls.url + '/file/upload/request', files=files)

            print(resp.text)

            print("status code " + str(resp.status_code))

            if resp.status_code == 200:
                print("Success")
                print(resp.json())
            else:
                print("Failure")

            f.close()
        except requests.exceptions.HTTPError as errh:
            print(errh)
        except requests.exceptions.ConnectionError as errc:
            print(errc)
        except requests.exceptions.Timeout as errt:
            print(errt)
        except requests.exceptions.RequestException as err:
            print(err)

    @classmethod
    def fileDownload(cls):
        try:
            # http://localhost:8080/downloadFile/%EC%95%84%EC%9D%B4%EC%BD%98.png
            time = TimeUtil.getNewTimeByLong()
            query = {'time': 1624862532320}
            response = requests.get(cls.url + '/file/download/trigger/trigger_06_42.csv', params=query)
            print(response.content)
            # print(response.text)
            # print(response)
        except requests.exceptions.HTTPError as errh:
            print(errh)
        except requests.exceptions.ConnectionError as errc:
            print(errc)
        except requests.exceptions.Timeout as errt:
            print(errt)
        except requests.exceptions.RequestException as err:
            print(err)


    @classmethod
    def deleteFile(cls):
        try:
            response = requests.post(cls.url + '/file/delete')
            # print(response)
        except requests.exceptions.HTTPError as errh:
            print(errh)
        except requests.exceptions.ConnectionError as errc:
            print(errc)
        except requests.exceptions.Timeout as errt:
            print(errt)
        except requests.exceptions.RequestException as err:
            print(err)

    @classmethod
    def fileSearch(cls):
        try:
            # http://localhost:8080/downloadFile/%EC%95%84%EC%9D%B4%EC%BD%98.png
            startOfDay = TimeUtil.getNewDate()
            startOfDay = TimeUtil.startOfDay(startOfDay)
            endOfDay = TimeUtil.getNewDate()
            endOfDay = TimeUtil.endOfDay(endOfDay)

            query = {
                'type': "accel",
                'startTime': TimeUtil.dateToLong(startOfDay),
                'endTime': TimeUtil.dateToLong(endOfDay)
            }

            print(query)

            response = requests.get(cls.url + '/file/find', params=query)
            # print(response.content)
            print(response.text)
            print(response)
        except requests.exceptions.HTTPError as errh:
            print(errh)
        except requests.exceptions.ConnectionError as errc:
            print(errc)
        except requests.exceptions.Timeout as errt:
            print(errt)
        except requests.exceptions.RequestException as err:
            print(err)


    @classmethod
    def jsonTest(cls):
        jstr = '{"measureId": 177003, "name": "1111", "createTime": "2021-06-15T01:23:56.440+00:00", "mode": "INTERVAL", "status": "ING"}'
        json_data = json.loads(jstr)
        print(json.dumps(json_data))

        # print(json_data['measureId'])
        # print(json_data['name'])

    @classmethod
    def setSetting(cls):
        try:
            query = {
                'accel': '1_5_100',
                'slope': '1_5_1',
                'triggerLevel': '1_3.5',
                'standardTime': '0_0',
                'request': '*RA10$'
            }
            response = requests.post(cls.url + '/measure/post/setting', params=query)
            print(response.text)
        except requests.exceptions.HTTPError as errh:
            print(errh)
        except requests.exceptions.ConnectionError as errc:
            print(errc)
        except requests.exceptions.Timeout as errt:
            print(errt)
        except requests.exceptions.RequestException as err:
            print(err)

    @classmethod
    def getSetting(cls):
        from python.serial.SerialManager import SerialManager
        try:
            response = requests.get(cls.url + '/measure/get/setting')
            jstr = response.text
            dic = json.loads(jstr)

            if (RequestApi.lastStringRequestTime >= dic['time']):
                return

            print(jstr)
            RequestApi.lastStringRequestTime = dic['time']
            accelList = dic['accel'].split('_')
            if len(accelList) == 3:
                SerialManager.accelMeasureHour = int(accelList[0])
                SerialManager.accelMeasureMin = int(accelList[1])
                SerialManager.accelIntervalPerSec = int(accelList[2])
                print('accel: %s'% dic['accel'])

            slopeList = dic['slope'].split('_')
            if len(slopeList) == 3:
                SerialManager.slopeMeasureHour = int(slopeList[0])
                SerialManager.slopeMeasureMin = int(slopeList[1])
                SerialManager.slopeIntervalPerSec = int(slopeList[2])
                print('slope: %s'% dic['slope'])

            triggerList = dic['triggerLevel'].split('_')
            if len(triggerList) == 2:
                SerialManager.abnormalXMin = int(triggerList[0])
                SerialManager.abnormalXMax = int(triggerList[1])
                print('triggerLevel: %s'% dic['triggerLevel'])

            timeList = dic['standardTime'].split('_')
            if len(timeList) == 2:
                TimeUtil.standardHour = int(timeList[0])
                TimeUtil.standardMin = int(timeList[1])
                print('standardTime: %s'% dic['standardTime'])

            request = dic['request']
            if '*RS' in request:
                instance = SerialManager.instance
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


# Test Code
if __name__ == "__main__":
    from RequestApi import RequestApi as api

    # api.setCompany()
    # api.findCompany()
    # api.start()
    # api.addMeasureItems()
    # api.getMeasureItems()
    # api.setSensorSetting()
    # api.getSensorItems()
    # api.fileUpload()
    # api.fileDownload()
    # api.deleteFile()
    # api.fileSearch()
    # api.jsonTest()
    # api.slopeRequestFileUpload()
    # api.accelRequestFileUpload()
    # api.setSetting()
    # api.getSetting()