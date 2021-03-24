import serial
import time
import signal
import threading

import wx

from util.test.test import CalcFrame

if __name__ == "__main__":
    app = wx.App(False)
    frame = CalcFrame(None)
    frame.Show(True)
    # start the applications
    app.MainLoop()