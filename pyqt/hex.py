########################################
#
# hex.py
#
# Description: creates a hexagonal grid
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
import random
from PyQt5.QtCore    import QObject, QPointF
from PyQt5.QtGui     import QFont, QPen, QColor, QBrush, QPolygonF, QPainter
from PyQt5.QtWidgets import QApplication, QToolTip, QWidget, QLabel,\
                            QPushButton, QDialog,QDesktopWidget

Point = collections.namedtuple('Point', 'x y')
r = lambda: random.randint(0,255)
s = lambda: '#%02X%02X%02X' % (r(),r(),r())
# s() #creates a random hex code for colors


class Hex:

    def __init__(self,q=0, r=0,size=50):
        self.q = q
        self.r = r
        self.size   = size
        self.width  = self.size*2*3/4
        self.height = math.sqrt(3)/4*self.size*2
        self.center = Point(self.q*self.width,
                            self.q*self.height+(self.r*self.height*2))

    def __repr__(self):
        return 'Hex(%r,%r,%r,%r)' % (self.q,self.r,self.size,self.center)

    def __add__(self,other):
        q = self.q + other.q
        r = self.r + other.r
        return Hex(q,r,self.size)

    def __sub__(self,other):
        q = self.q - other.q
        r = self.r - other.r
        return Hex(q,r,self.size)

    def hex_corner(self,center,size,i):
        angle_deg = 60*i
        return Point(center[0]+size*math.cos(math.radians(angle_deg)),
                     center[1]+size*math.sin(math.radians(angle_deg)))


class window(QDialog):

    def __init__(self):
        super(window,self).__init__()
        self.initUI()
        self.initBoard()
        self.initShow()

    def initUI(self):

        self.radius = 5
        self.polygonsize = 50
        self.windowSize = Hex(0,0,self.polygonsize).width*(2*self.radius+3)
        self.resize(self.windowSize,self.windowSize)
        self.center
        self.setWindowTitle("PyQt - Hex Board")

    def initBoard(self):
        self.pen = QPen(QColor(0,0,0))                      # set lineColor
        self.pen.setWidth(3)                                # set lineWidth
        # self.brush = QBrush(QColor(255,255,255,255))        # set fillColor

    def initShow(self):
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def createPoly(self,item):
        polygon = QPolygonF()
        for i in range(6): # add the points of polygon
            coords = item.hex_corner(item.center,item.size,i)
            polygon.append(QPointF(self.windowSize/2+coords.x,
                                   self.windowSize/2-2*item.center.y+coords.y))

        return polygon

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(self.pen)
        # painter.setBrush(self.brush)
        iter=0
        for i in range(-self.radius,self.radius+1):
            for j in range(-self.radius,self.radius+1):
                if (abs(i+j) <= self.radius):
                    self.brush = QBrush(QColor(s()))
                    iter+=1
                    painter.setBrush(self.brush)
                    polygon = self.createPoly(Hex(i,j,self.polygonsize))
                    painter.drawPolygon(polygon)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = window()
    sys.exit(app.exec_())
