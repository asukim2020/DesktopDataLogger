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

from python.serial.SerialManager import SerialManager

if __name__ == "__main__":
    import socket

    from requests import get
    ip = get('https://api.ipify.org')
    print(f'{ip.text}')

    # Linux add path
    # import sys
    # sys.path.append("/home/pi/Documents/DesktopDataLogger/python/serial")
    # print(sys.path)
    #
    # serial = SerialManager()
    # serial.start()
    # serial.end()

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
