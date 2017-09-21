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

    def __init__(self,q=0, r=0, s=0,size=10,center=(0,0,0)):
        self.q = q
        self.r = r
        self.s = s
        self.size = size
        self.center = center

    def __repr__(self):
        return 'Hex(%r,%r,%r,%r,%r)' % (self.q,self.r,self.s,self.size,self.center)

    def __add__(self,other):
        q = self.q + other.q
        r = self.r + other.r
        s = self.s + other.s
        return Hex(q,r,s,self.size)

    def __sub__(self,other):
        q = self.q - other.q
        r = self.r - other.r
        s = self.s - other.s
        return Hex(q,r,s,self.size)

    def hex_corner(self,center,size,i):
        angle_deg = 60*i
        return Point(center[0]+size*math.cos(math.radians(angle_deg)),
                     center[0]+size*math.sin(math.radians(angle_deg)))

h=Hex(1,2,3)
print(h)
print(Hex(1,-3,2)+Hex(3,-7,4))
print(Hex(1,-3,2)-Hex(3,-7,4))
print(h.size)
for i in range(6):
    print(h.hex_corner((15,17.3205),10,i))

width = 50*2*3/4
height = -math.sqrt(3)/4*50*2

print(width,height)
print('------')
q=3
r=-1
print(q*width,-q*height-(r*height*2))
q=1
r=0
print(q*width,-q*height-(r*height*2))

class window(QDialog):

    def __init__(self):
        super(window,self).__init__()
        self.initUI()

    def initUI(self):

        self.resize(500,500)
        self.center
        self.setWindowTitle("PyQt")
        self.pen = QPen(QColor(0,0,0))                      # set lineColor
        self.pen.setWidth(3)                                            # set lineWidth
        self.brush = QBrush(QColor(255,255,255,255))        # set fillColor
        self.polygon = self.createPoly(0,0)                         # polygon with n points, radius, angle of the first point
        self.polygon2 = self.createPoly(width,-height)
        self.polygon3 = self.createPoly(2*width,-2*height-(-1*height*2))
        self.polygon4 = self.createPoly(3*width,-3*height-(-1*height*2))
        print(3*width,-3*height-(-1*height*2))
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def createPoly(self,this,that):
        polygon = QPolygonF()
        h = Hex(0,0,0,50)                                                     # angle per step
        for i in range(6):                                              # add the points of polygon
            angle_deg = 60*i
            size = h.size
            x = size*math.cos(math.radians(angle_deg))
            y = size*math.sin(math.radians(angle_deg))
            center = (this+250,that+250)
            # print(size*(3/2)+h.q,h.size*math.sqrt(3)*(h.r +h.q/2))
            # print(self.width()/2 +x,350*math.cos(math.pi/180*60*i))
            # print(350*math.cos(math.pi/180*60*i),350*math.sin(math.pi/180*60*i))
            polygon.append(QPointF(center[0]+x,center[1]+y))

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
