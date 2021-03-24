import asyncio
import time

import wx

from util.eventbus.GlobalBus import GlobalBus
from util.eventbus.HashMapEvent import HashMapEvent
from util.serial.SerialManager import SerialManager


# async def say_after(delay, what):
#     for i in range(0, 10):
#         await asyncio.sleep(delay)
#         print(what)
#
#
# async def main():
#     task1 = asyncio.create_task(
#         say_after(0.1, 'hello'))
#
#     task2 = asyncio.create_task(
#         say_after(0.1, 'world'))
#
#     print(f"started at {time.strftime('%X')}")
#
#     # Wait until both tasks are completed (should take
#     # around 2 seconds.)
#     await task1
#     await task2
#
#     print(f"finished at {time.strftime('%X')}")
#
#
# if __name__ == "__main__":
#     asyncio.run(main())
#     print("main end")


# class CalcFrame(demo.MyFrame1):
#     def __init__(self, parent):
#         demo.MyFrame1.__init__(self, parent)
#
#     def FindSquare(self, event):
#         num = int(self.m_textCtrl1.GetValue())
#         self.m_textCtrl2.SetValue(str(num * num))
#
#
# if __name__ == "__main__":
#     app = wx.App(False)
#     frame = CalcFrame(None)
#     frame.Show(True)
#     # start the applications
#     app.MainLoop()
from util.test import serial_test


class CalcFrame(serial_test.MyFrame4):
    def __init__(self, parent):
        serial_test.MyFrame4.__init__(self, parent)

        self.serialManager = SerialManager()

    def clickStart(self, event):
        self.serialManager.start()

    def clickEnd(self, event):
        self.serialManager.end()

    @staticmethod
    def toString():
        return "CalcFrame"


if __name__ == "__main__":
    app = wx.App(False)
    frame = CalcFrame(None)
    frame.Show(True)
    # start the applications
    app.MainLoop()
