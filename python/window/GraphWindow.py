import numpy
import pyqtgraph
from PyQt5.QtWidgets import *
from PyQt5 import uic
from python.serial.SerialManager import SerialManager

form_class = uic.loadUiType("python/layout/graph.ui")[0]


class GraphWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.serialManager = SerialManager()

        self.startButton.clicked.connect(self.clickStart)
        self.endButton.clicked.connect(self.clickEnd)

        self.channelCount = 2
        self.size = 10

        self.dataList = []
        self.curveList = []
        self.ptr = 0

        for idx in range(self.channelCount):
            self.dataList.append([])
        self.curveList.append(self.widget.plot(self.dataList[0], name="mode2", pen='b', symbolBrush='b'))
        self.curveList.append(self.widget.plot(self.dataList[1], name="mode2", pen='r', symbolBrush='r'))

        self.timer = pyqtgraph.QtCore.QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.start(100)

    def update_data(self):
        flag = True
        for idx in range(len(self.dataList)):
            data = self.dataList[idx]
            curve = self.curveList[idx]

            if self.size < len(data):
                data[:-1] = data[1:]
                data[-1] = numpy.random.normal()
                if flag:
                    self.ptr += 1
                    flag = False
            else:
                data.append(numpy.random.normal())
            curve.setData(data)
            curve.setPos(self.ptr, 0)

    def clickStart(self, event):
        self.serialManager.start(self)

    def clickEnd(self, event):
        self.serialManager.end()

    def setText(self, text):
        print()
        # widget
        # set data
