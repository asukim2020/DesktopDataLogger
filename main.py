import datetime
import sys
# from PyQt5.QtWidgets import *
#
# from python.window.DemoWindow import DemoWindow

# demo window
# if __name__ == "__main__":
    # app = QApplication(sys.argv)
    # myWindow = DemoWindow()
    # myWindow.showNormal()
    # myWindow.showMaximized()
    # myWindow.showFullScreen()
    # app.exec_()


# from python.window.GraphWindow import GraphWindow
#
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     myWindow = GraphWindow()
#     myWindow.show()
#     # myWindow.showMaximized()
#     # myWindow.showFullScreen()
#     app.exec_()

import datetime as dt
import time
import datetime

from python.serial.MeasureSetting import MeasureSetting
from python.serial.SerialManager import SerialManager
from python.serial.TCPServer import TCPServer
from python.serial.RequestApi import RequestApi as api
from python.serial.TimeUtil import TimeUtil

if __name__ == "__main__":
    import socket

    # from requests import get
    # ip = get('https://api.ipify.org')
    # print(f'{ip.text}')

    # Linux add path
    import sys
    sys.path.append("/home/pi/Documents/DesktopDataLogger/python/serial")
    print(sys.path)

    serial = SerialManager()
    # serial.saveSettingData()
    # serial.getSettingData()
    serial.start()
    # TimeUtil.getSettingData()
    SerialManager.instance = serial
    # serial.end()

    # server = TCPServer()
    # server.startServer()

    setting = MeasureSetting()
    setting.start()

    # from python.serial.TimeUtil import TimeUtil
    # t1 = TimeUtil.getNewTimeByLong()
    # print(t1)
    #
    # date = TimeUtil.getNextDay(t1, 1)
    # t2 = TimeUtil.dateToLong(date)
    # print((t2%3600000)/60000)


    # print(t2 - t1)
    # print((t2 - t1)/24/60/60/1000)

    # t = time.time()
    # float
    # print(int(t * 1000 % 0xFFFFFFFFFFFFFFFF))

    # date = datetime.datetime.fromtimestamp(t)

    # start of day
    # date = date.replace(hour=0, minute=0, second=0, microsecond=0)

    # end of day
    # date = date.replace(hour=0, minute=0, second=0, microsecond=0)
    # date += datetime.timedelta(days=1, milliseconds=-1)

    # next day
    # date += datetime.timedelta(days=0)

    # print(date)
    # print(date.timestamp())
