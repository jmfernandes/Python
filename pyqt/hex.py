########################################
#
# hex.py
#
# Description:
#
#
# Author: Josh Fernandes
#
# Created: Sep 21, 2017
#
# Updated:
#
#
########################################
import sys
import collections
import math
from PyQt5.QtCore import QObject
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QToolTip, QWidget, QLabel, QPushButton, QDialog

class Hex:

    def __init__(self, q=0, r=0, s=0):
        self.q = q
        self.r = r
        self.s = s

    def __repr__(self):
        return 'Hex(%r,%r,%r)' % (self.q,self.r,self.s)

class window(QDialog):

    def __init__(self):
        super(window,self).__init__()
        self.initUI()

    def initUI(self):

        self.resize(500,150)
        self.center
        self.setWindowTitle("PyQt")
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = window()
    sys.exit(app.exec_())
