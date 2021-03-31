import sys
from PyQt5.QtWidgets import *

from python.window.DemoWindow import DemoWindow

# demo window
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     myWindow = DemoWindow()
#     myWindow.showMaximized()
#     # myWindow.showFullScreen()
#     app.exec_()
from python.window.GraphWindow import GraphWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = GraphWindow()
    myWindow.show()
    # myWindow.showMaximized()
    # myWindow.showFullScreen()
    app.exec_()