from io import StringIO

import requests
import json


class RequestApi:

    def __init__(self):
        super().__init__()

        self.url = 'http://3.37.113.193:8080/'
        # self.url = 'http://localhost:8080'

    def start(self):
        # mode -> "step" or "interval"
        query = {'name': '12345'}
        response = requests.post(self.url + '/measure/post/start', params=query)

        jstr = StringIO(response.text)
        json_data = json.load(jstr)
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
    api.getMeasureItems()
