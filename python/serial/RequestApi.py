from io import StringIO

import requests
import json


# TODO: - 라즈베리에서 15.csv 파일을 받아 업로드 해서 속도가 얼만나 나오는지 테스트
# TODO: - 즉, 모뎀의 인터넷 속도가 얼마인지 알아보기

# TODO: - 초당 100 개 인 경우 받
from python.serial.TimeUtil import TimeUtil


class RequestApi:
    url = 'http://3.37.113.193:8080/'
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
    def findCompany(cls):
        try:
            ip = requests.get('https://api.ipify.org')

            query = {
                'name': 'NGI'
            }
            response = requests.get(cls.url + '/measure/get/company/name', params=query)
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
            # 설정 시작 명령어
            sendStringList.append("*U")

            # 채널 번호 2자리
            sendStringList.append(item["number"])

            # on: 1, off: 0 1자리
            sendStringList.append("1")

            # 센서 종료 2자리
            sendStringList.append(item["type"])

            # 엠프게인 1자리
            sendStringList.append(item["ampGain"])

            # 인가전압 1자리
            sendStringList.append(item["applyV"])

            # 필터 1자리리
            sendStringList.append(item["filter"])

            # 종료 문자
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
    def accelFileUpload(cls):
        try:
            f = open('accel.csv', 'rb')
            files = {"file": f}
            resp = requests.post(cls.url + '/file/upload/accel', files=files)
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
    def triggerFileUpload(cls):
        try:
            f = open('trigger.csv', 'rb')
            files = {"file": f}
            resp = requests.post(cls.url + '/file/upload/trigger', files=files)
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
    def requestFileUpload(cls):
        try:
            f = open('request.csv', 'rb')
            files = {"file": f}
            resp = requests.post(cls.url + '/file/upload/request', files=files)
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
    def fileUpload(cls):
        try:
            f = open('C:/Users/Asu/Downloads/앱이미지2/015.csv', 'rb')

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
    def fileSearch(cls):
        try:
            # http://localhost:8080/downloadFile/%EC%95%84%EC%9D%B4%EC%BD%98.png
            time = TimeUtil.getNewTimeByLong()
            startOfDay = TimeUtil.getNewDate()
            startOfDay = TimeUtil.startOfDay(startOfDay)
            endOfDay = TimeUtil.getNewDate()
            endOfDay = TimeUtil.endOfDay(endOfDay)

            query = {
                'type': "trigger",
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


# Test Code
if __name__ == "__main__":
    from RequestApi import RequestApi as api

    api.setCompany()
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
