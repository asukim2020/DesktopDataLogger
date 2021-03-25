# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class MyFrame4
###########################################################################
from util.eventbus.GlobalBus import GlobalBus, subscribe, Mode, threading
from util.eventbus.HashMapEvent import HashMapEvent
from util.serial.SerialManager import SerialManager


class MyFrame4(wx.Frame):

    def __init__(self, parent):
        GlobalBus.register(self)
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition,
                          size=wx.Size(606, 530), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        bSizer2 = wx.BoxSizer(wx.VERTICAL)

        self.btn_start = wx.Button(self, wx.ID_ANY, u"Start", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer2.Add(self.btn_start, 0, wx.ALL | wx.EXPAND, 5)

        self.btn_end = wx.Button(self, wx.ID_ANY, u"End", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer2.Add(self.btn_end, 0, wx.ALL | wx.EXPAND, 5)

        self.tv = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE)
        bSizer2.Add(self.tv, 1, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(bSizer2)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.btn_start.Bind(wx.EVT_BUTTON, self.clickStart)
        self.btn_end.Bind(wx.EVT_BUTTON, self.clickEnd)

    def __del__(self):
        pass

    @subscribe(threadMode=Mode.BACKGROUND, onEvent=HashMapEvent)
    def func(self, event):
        serialManager = event.map.get(SerialManager.toString())
        if serialManager is not None:
            line = event.map.get("line")

            if line is not None:
                tmp = ''.join(line)
                print(tmp)
                self.tv.AppendText(tmp)


    # Virtual event handlers, overide them in your derived class
    def clickStart(self, event):
        event.Skip()

    def clickEnd(self, event):
        event.Skip()
