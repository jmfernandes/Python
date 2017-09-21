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
from PyQt5.QtCore import QObject, QPointF
from PyQt5.QtGui import QFont, QPen, QColor, QBrush, QPolygonF, QPainter
from PyQt5.QtWidgets import QApplication, QToolTip, QWidget, QLabel,\
                            QPushButton, QDialog

Point = collections.namedtuple('Point', 'x y')

class Hex:

    def __init__(self,q=0, r=0,size=50):
        self.q = q
        self.r = r
        self.size   = size
        self.width  = self.size*2*3/4
        self.height = math.sqrt(3)/4*self.size*2
        self.center = Point(self.q*self.width,self.q*self.height+(self.r*self.height*2))

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

# h=Hex(1,2,3)
# print(h)
# print(Hex(1,-3,2)+Hex(3,-7,4))
# print(Hex(1,-3,2)-Hex(3,-7,4))
# print(h.size)
# for i in range(6):
#     print(h.hex_corner((15,17.3205),10,i))
h = Hex(0,0)
print(h)
print(h.center.x,h.center.y)
print(h.width)
print(h.height)
print(h.hex_corner(h.center,h.size,3).x)

width = 50*2*3/4
height = -math.sqrt(3)/4*50*2

# print(width,height)
# print('------')
# q=3
# r=-1
# print(q*width,-q*height-(r*height*2))
# q=1
# r=0
# print(q*width,-q*height-(r*height*2))

class window(QDialog):

    def __init__(self):
        super(window,self).__init__()
        self.initUI()
        self.initBoard()
        self.initShow()

    def initUI(self):

        self.resize(500,500)
        self.center
        self.setWindowTitle("PyQt")

    def initBoard(self):
        self.pen = QPen(QColor(0,0,0))                      # set lineColor
        self.pen.setWidth(3)                                            # set lineWidth
        self.brush = QBrush(QColor(255,255,255,255))        # set fillColor
        self.polygon = self.createPoly(Hex(0,0))                         # polygon with n points, radius, angle of the first point
        self.polygon2 = self.createPoly(Hex(1,0))
        self.polygon3 = self.createPoly(Hex(0,1))
        self.polygon4 = self.createPoly(Hex(1,1))

    def initShow(self):
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def createPoly(self,item):
        polygon = QPolygonF()                                                    # angle per step
        for i in range(6):                                              # add the points of polygon
            # angle_deg = 60*i
            # size = item.size
            # x = size*math.cos(math.radians(angle_deg))
            # y = size*math.sin(math.radians(angle_deg))
            # center = (item.center.x+250,250-item.center.y)
            cords = item.hex_corner(item.center,item.size,i)
            # print(y,cords.y-item.center.y)
            # print(center[1]+y,250-2*item.center.y+cords.y)
            # print(center[0]+x,250+cords.x)
            polygon.append(QPointF(250+cords.x,250-2*item.center.y+cords.y))

        return polygon

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(self.pen)
        painter.setBrush(self.brush)
        painter.drawPolygon(self.polygon)
        painter.drawPolygon(self.polygon2)
        painter.drawPolygon(self.polygon3)
        painter.drawPolygon(self.polygon4)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = window()
    sys.exit(app.exec_())
