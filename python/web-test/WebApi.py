import random
from datetime import datetime

import requests
import json

class WebApi:
    url = 'http://localhost:8080'
    companyId = -1
    dataLoggerList = []

    def __init__(self):
        super(WebApi, self).__init__()



    @classmethod
    def login(cls):
        try:
            query = {
                'id': 'test',
                'pw': 'test!'
            }
            response = requests.post(cls.url + '/company/login', params=query)
            WebApi.companyId = int(response.text)
            print(WebApi.companyId)

        except requests.exceptions.HTTPError as errh:
            print(errh)
        except requests.exceptions.ConnectionError as errc:
            print(errc)
        except requests.exceptions.Timeout as errt:
            print(errt)
        except requests.exceptions.RequestException as err:
            print(err)

    @classmethod
    def getDataLoggerList(cls):
        try:
            response = requests.get(cls.url + '/dataLogger/' + str(WebApi.companyId))
            jstr = response.text
            json_data = json.loads(jstr)
            WebApi.dataLoggerList.clear()
            for data in json_data:
              WebApi.dataLoggerList.append(data['id'])

        except requests.exceptions.HTTPError as errh:
            print(errh)
        except requests.exceptions.ConnectionError as errc:
            print(errc)
        except requests.exceptions.Timeout as errt:
            print(errt)
        except requests.exceptions.RequestException as err:
            print(err)

    @classmethod
    def uploadDatas(cls, dataLoggerId):
        try:
            measureDataDtos = []
            datas = []
            now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")[0:23]
            for i in range(0, 3):
                data = str(int(random.random() * 30))
                datas.append(data)
            dataString = ','.join(datas)
            print(dataString)

            measureDataDtos.append({
                'data': dataString,
                'time': now
            })
            print(measureDataDtos)
            response = requests.post(cls.url + '/measureData/' + str(dataLoggerId), json=measureDataDtos)
            print(response)

        except requests.exceptions.HTTPError as errh:
            print(errh)
        except requests.exceptions.ConnectionError as errc:
            print(errc)
        except requests.exceptions.Timeout as errt:
            print(errt)
        except requests.exceptions.RequestException as err:
            print(err)

if __name__ == "__main__":
    from WebApi import WebApi as api
    api.login()
    api.getDataLoggerList()
    for _ in range(0, 10):
        for dataLoggerId in api.dataLoggerList:
            api.uploadDatas(dataLoggerId)