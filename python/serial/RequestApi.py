from io import StringIO

import requests
import json


class RequestApi:


    def __init__(self):
        super().__init__()

        # self.url = 'http://3.37.113.193:8080/'
        self.url = 'http://localhost:8080'
        # self.url = 'http://211.184.136.231:8080'


    def start(self):
        # mode -> "step" or "interval"
        query = {'name': '12345'}
        response = requests.post(self.url + '/measure/post/start', params=query)

        jstr = response.text
        json_data = json.loads(jstr)
        id = json_data['measureId']
        print(id)
        print(json_data['name'])

        return id


    def addMeasureItem(self):
        id = 1
        obj = []
        for i in range(0, 3):
            dic = {}
            dic["data"] = "*+1234+1234+1234$"
            dic["time"] = 1623892415373 + (10000 * i)
            obj.append(dic)

        query = {'id': id}
        response = requests.post(self.url + "/measure/post/items", params=query, json=obj)
        print(response)
        print(response.text)

        # jstr = StringIO('['
        #                 '{"data": "*+1234+1234+1234$","time": 1623892395373},'
        #                 '{"data": "*+1234+1234+1234$","time": 1623892405373},'
        #                 '{"data": "*+1234+1234+1234$","time": 1623892415373}'
        #                 ']'
        #                 )

        # json_data = json.load(jstr)
        # query = {'id': id}
        # requests.post(self.url + "/measure/post/items", params=query, json=json_data)


    def getMeasureItems(self):
        query = {
            'id': 1,
            'startTime': 1623892415373,
            'endTime': 1623892435373,
            'afterId': 0
        }
        response = requests.get(self.url + '/measure/get/items/time', params=query)
        print(response)
        jstr = response.text
        json_data = json.loads(jstr)
        print(json.dumps(json_data, indent=4))


    def setSensorSetting(self):
        id = 1
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
        response = requests.post(self.url + "/measure/sensor/set/list", params=query, json=obj)
        print(response)
        print(response.text)


    def getSensorItems(self):
        query = {'id': '1'}
        response = requests.get(self.url + '/measure/sensor/get/list', params=query)

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


    def fileUpload(self):
        f = open('C:/Users/Asu/Downloads/앱이미지2/아이콘.png', 'rb')

        files = {"file": f}

        resp = requests.post(self.url + '/uploadFile', files=files)

        print(resp.text)

        print("status code " + str(resp.status_code))

        if resp.status_code == 200:
            print("Success")
            print(resp.json())
        else:
            print("Failure")


    def fileDownload(self):
        # http://localhost:8080/downloadFile/%EC%95%84%EC%9D%B4%EC%BD%98.png
        response = requests.get(self.url + '/downloadFile/아이콘.png')
        print(response.content)
        print(response.text)
        print(response)


    def jsonTest(self):
        jstr = '{"measureId": 177003, "name": "1111", "createTime": "2021-06-15T01:23:56.440+00:00", "mode": "INTERVAL", "status": "ING"}'
        json_data = json.loads(jstr)

        print(json_data['measureId'])
        print(json_data['name'])


# Test Code
if __name__ == "__main__":
    api = RequestApi()
    # api.start()
    # api.jsonTest()
    # api.addMeasureItem()
    # api.getMeasureItems()
    # api.setSensorSetting()
    # api.getSensorItems()
    # api.fileUpload()
    # api.fileDownload()
