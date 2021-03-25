# import wx
#
# from util.test.test import CalcFrame
#
# if __name__ == "__main__":
#     app = wx.App(False)
#     frame = CalcFrame(None)
#     frame.Show(True)
#     # start the applications
#     app.MainLoop()


import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from util.serial.SerialManager import SerialManager
from util.eventbus.GlobalBus import GlobalBus, subscribe, Mode, threading
from util.eventbus.HashMapEvent import HashMapEvent

form_class = uic.loadUiType("demo.ui")[0]


class DemoWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        GlobalBus.register(self)
        self.serialManager = SerialManager()

        self.startButton.clicked.connect(self.clickStart)
        self.endButton.clicked.connect(self.clickEnd)

    def clickStart(self, event):
        self.serialManager.start()

    def clickEnd(self, event):
        self.serialManager.end()

    @subscribe(threadMode=Mode.BACKGROUND, onEvent=HashMapEvent)
    def func(self, event):
        serialManager = event.map.get(SerialManager.toString())
        if serialManager is not None:
            line = event.map.get("line")

            if line is not None:
                tmp = ''.join(line)
                print(tmp)
                self.tv.append(tmp)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = DemoWindow()
    myWindow.show()
    app.exec_()
