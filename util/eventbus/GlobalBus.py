from pyeventbus3.pyeventbus3 import *


class GlobalBus:
    sBus = PyBus.Instance()

    @staticmethod
    def register(myclass):
        GlobalBus.sBus.register(myclass, myclass.__class__.__name__)

    @staticmethod
    def post(event):
        GlobalBus.sBus.post(event)
