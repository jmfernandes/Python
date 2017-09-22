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
Cube = collections.namedtuple('Cube', 'x y z')
r = lambda: random.randint(0,255)
s = lambda: '#%02X%02X%02X' % (r(),r(),r())
# s() #creates a random hex code for colors

def pixel_to_hex(x,y,size):
    q = round(-x * 2/3 / size)
    r = round((x / 3 + math.sqrt(3)/3 * y) / size)
    return Hex(q,r,size)

def hex_to_pixel(hex):
    x = hex.size*3/2*hex.q
    y = hex.size*(hex.r+hex.q/2)
    return Point(x,y)

def distance(a):
    if (a.q == a.r):
        return abs(a.q+a.r)
    else:
        return (abs(a.q) + abs(a.r))

def axial_to_cube(hex):
    x = hex.q
    z = hex.r
    y = -x-z
    return Cube(x, y, z)

def cube_distance(a, b):
    return (abs(a.x - b.x) + abs(a.y - b.y) + abs(a.z - b.z)) / 2

def hex_distance(a, b):
    ac = axial_to_cube(a)
    bc = axial_to_cube(b)
    return cube_distance(ac, bc)

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
        return Point(center.x+size*math.cos(math.radians(angle_deg)),
                     center.y+size*math.sin(math.radians(angle_deg)))

class window(QDialog):

    def __init__(self):
        super(window,self).__init__()
        self.initUI()

    def initUI(self):

        self.iteration = 0
        self.mouse = Point(0,0)
        self.redcoords = Point(0,0)
        self.bluecoords = Point(0,0)
        self.radius = 2
        self.polygonsize = 50
        self.windowSize = Hex(0,0,self.polygonsize).width*(2*self.radius+3.5)
        self.resize(self.windowSize,self.windowSize)
        self.center
        self.setWindowTitle("PyQt - Hex Board")
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

    def reset(self):
        self.redcoords = Point(0,0)
        self.bluecoords = Point(0,0)
        self.iteration=1

    def mousePressEvent(self,QMouseEvent):
        pos = QMouseEvent.pos()
        x = self.windowSize/2 - QMouseEvent.x()
        y = self.windowSize/2 - QMouseEvent.y()
        self.mouse = Point(pixel_to_hex(x,y,self.polygonsize).q,pixel_to_hex(x,y,self.polygonsize).r)
        self.iteration+=1
        if self.iteration>3: #reset the board
            self.reset()
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        self.pen = QPen(QColor(0,0,0))                      # set lineColor
        self.pen.setWidth(3)                                # set lineWidth
        painter.setPen(self.pen)
        distance = hex_distance(Hex(self.mouse.x,self.mouse.y),Hex(0,0))
        if self.iteration == 0:
            for i in range(-self.radius,self.radius+1):
                for j in range(-self.radius,self.radius+1):
                    if (abs(i+j) <= self.radius):
                        self.brush = QBrush(QColor(255,255,255,255))
                        painter.setBrush(self.brush)
                        polygon = self.createPoly(Hex(i,j,self.polygonsize))
                        painter.drawPolygon(polygon)
        elif self.iteration == 1:
            if distance > self.radius: #not valid hex chosen
                for i in range(-self.radius,self.radius+1):
                    for j in range(-self.radius,self.radius+1):
                        if (abs(i+j) <= self.radius):
                                #draw remainder of white hexes
                                self.brush = QBrush(QColor(255,255,255,255))
                                painter.setBrush(self.brush)
                                polygon = self.createPoly(Hex(i,j,self.polygonsize))
                                painter.drawPolygon(polygon)
                                self.iteration = 0 #reset to redraw red hex
            else: #valid hex choses
                for i in range(-self.radius,self.radius+1):
                    for j in range(-self.radius,self.radius+1):
                        if (abs(i+j) <= self.radius):
                            if (i == self.mouse.x and j == self.mouse.y):
                                #draw red hex
                                self.redcoords = Point(i,j)
                                self.brush = QBrush(QColor(255,0,0,255))
                                painter.setBrush(self.brush)
                                polygon = self.createPoly(Hex(i,j,self.polygonsize))
                                painter.drawPolygon(polygon)
                            else:
                                #draw remainder of white hexes
                                self.brush = QBrush(QColor(255,255,255,255))
                                painter.setBrush(self.brush)
                                polygon = self.createPoly(Hex(i,j,self.polygonsize))
                                painter.drawPolygon(polygon)
        elif self.iteration == 2:
            if distance > self.radius: #not valid hex chosen
                for i in range(-self.radius,self.radius+1):
                    for j in range(-self.radius,self.radius+1):
                        if (abs(i+j) <= self.radius):
                            if (i == self.redcoords.x and j == self.redcoords.y):
                                #redraws the old red hex
                                self.brush = QBrush(QColor(255,0,0,255))
                                painter.setBrush(self.brush)
                                polygon = self.createPoly(Hex(i,j,self.polygonsize))
                                painter.drawPolygon(polygon)
                            else:
                                #draw the remainder white hex
                                self.brush = QBrush(QColor(255,255,255,255))
                                painter.setBrush(self.brush)
                                polygon = self.createPoly(Hex(i,j,self.polygonsize))
                                painter.drawPolygon(polygon)
                            self.iteration = 1
            else:
                for i in range(-self.radius,self.radius+1):
                    for j in range(-self.radius,self.radius+1):
                        if (abs(i+j) <= self.radius):
                            if (self.mouse.x == self.redcoords.x and self.mouse.y == self.redcoords.y ):
                                #undo red hex
                                self.iteration=0
                                self.brush = QBrush(QColor(255,255,255,255))
                                painter.setBrush(self.brush)
                                polygon = self.createPoly(Hex(i,j,self.polygonsize))
                                painter.drawPolygon(polygon)
                            elif (i == self.mouse.x and j == self.mouse.y):
                                #draws blue hex
                                self.bluecoords = Point(i,j)
                                self.brush = QBrush(QColor(0,0,255,255))
                                painter.setBrush(self.brush)
                                polygon = self.createPoly(Hex(i,j,self.polygonsize))
                                painter.drawPolygon(polygon)
                            elif (i == self.redcoords.x and j == self.redcoords.y):
                                #redraws the old red hex
                                self.brush = QBrush(QColor(255,0,0,255))
                                painter.setBrush(self.brush)
                                polygon = self.createPoly(Hex(i,j,self.polygonsize))
                                painter.drawPolygon(polygon)
                            else:
                                #draw the remainder white hex
                                self.brush = QBrush(QColor(255,255,255,255))
                                painter.setBrush(self.brush)
                                polygon = self.createPoly(Hex(i,j,self.polygonsize))
                                painter.drawPolygon(polygon)
        elif self.iteration == 3:
            for i in range(-self.radius,self.radius+1):
                for j in range(-self.radius,self.radius+1):
                    if (abs(i+j) <= self.radius):
                        if (self.mouse.x == self.bluecoords.x and self.mouse.y == self.bluecoords.y ):
                            #undo red hex
                            self.iteration=1
                            self.brush = QBrush(QColor(255,255,255,255))
                            painter.setBrush(self.brush)
                            polygon = self.createPoly(Hex(i,j,self.polygonsize))
                            painter.drawPolygon(polygon)
                            if (i == self.redcoords.x and j == self.redcoords.y):
                                #redraws the old red hex
                                self.brush = QBrush(QColor(255,0,0,255))
                                painter.setBrush(self.brush)
                                polygon = self.createPoly(Hex(i,j,self.polygonsize))
                                painter.drawPolygon(polygon)
                        else:
                            self.brush = QBrush(QColor(255,255,255,255))
                            painter.setBrush(self.brush)
                            polygon = self.createPoly(Hex(i,j,self.polygonsize))
                            painter.drawPolygon(polygon)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = window()
    sys.exit(app.exec_())
