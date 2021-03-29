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
from python.serial.SerialManager import SerialManager

form_class = uic.loadUiType("python/layout/demo.ui")[0]


class DemoWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.serialManager = SerialManager()

        self.startButton.clicked.connect(self.clickStart)
        self.endButton.clicked.connect(self.clickEnd)

    def clickStart(self, event):
        self.serialManager.start(self)

    def clickEnd(self, event):
        self.serialManager.end()

    def setText(self, text):
        self.tv.append(text)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = DemoWindow()
    myWindow.show()
    app.exec_()
