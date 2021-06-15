from io import StringIO

import requests
import json


class RequestApi:

    def __init__(self):
        super().__init__()

        self.url = 'http://3.37.113.193:8080/'

    def start(self):
        # mode -> "step" or "interval"
        query = {'name': '1111', 'mode': 'interval'}
        response = requests.post(self.url + '/measure/post/start', params=query)
        jstr = StringIO(response.text)

        print(jstr)
        json_data = json.load(jstr)
        id = json_data['measureId']
        print(id)
        print(json_data['name'])

        return id

    def addMeasureItem(self):
        id = 177013
        jstr = StringIO('[{"count":1111,"data":"*+1234+1234+1234$","measureCount":0,"stepp":0,"elapsedTime":"00:00:00"},{"count":1111,"data":"*+1234+1234+1234$","measureCount":0,"stepp":0,"elapsedTime":"00:00:00"},{"count":1111,"data":"*+1234+1234+1234$","measureCount":0,"stepp":0,"elapsedTime":"00:00:00"}]')
        json_data = json.load(jstr)

        query = {'id': 177013}
        requests.post(self.url + "/measure/post/items", params=query, json=json_data)

    def jsonTest(self):
        io = StringIO(
            '{"measureId": 177003, "name": "1111", "createTime": "2021-06-15T01:23:56.440+00:00", "mode": "INTERVAL", "status": "ING"}')
        json_data = json.load(io)

        print(json_data['measureId'])
        print(json_data['name'])


# Test Code
if __name__ == "__main__":
    api = RequestApi()
    # api.start()
    # api.jsonTest()
    api.addMeasureItem()
