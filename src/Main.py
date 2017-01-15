import sys

from Controllers.WelcomeController import WelcomeController

from PyQt5.Qt import *

app = QApplication(sys.argv)

wc = WelcomeController()
wc.show()

app.exec_()
