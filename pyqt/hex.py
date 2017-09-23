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

def axial_to_cube(hex):
    x = hex.q
    z = hex.r
    y = -x-z
    return Cube(x, y, z)

def cube_to_axial(cube):
    q = cube.x
    r = cube.z
    return Hex(q, r)

def cube_distance(a, b):
    return (abs(a.x - b.x) + abs(a.y - b.y) + abs(a.z - b.z)) / 2

def hex_distance(a, b):
    ac = axial_to_cube(a)
    bc = axial_to_cube(b)
    return cube_distance(ac, bc)

def cube_round(cube):
    rx = round(cube.x)
    ry = round(cube.y)
    rz = round(cube.z)

    x_diff = abs(rx - cube.x)
    y_diff = abs(ry - cube.y)
    z_diff = abs(rz - cube.z)

    if x_diff > y_diff and x_diff > z_diff:
        rx = -ry-rz
    elif y_diff > z_diff:
        ry = -rx-rz
    else:
        rz = -rx-ry

    return Cube(rx, ry, rz)

def lerp(a, b, t):
    return a + (b - a) * t

def cube_lerp(a, b, t):
    return Cube(lerp(a.x, b.x, t),
                lerp(a.y, b.y, t),
                lerp(a.z, b.z, t))

def cube_linedraw(a, b): # pass in hex
    a = axial_to_cube(a)
    b = axial_to_cube(b)
    N = round(cube_distance(a, b))
    results = []
    for i in range(0,N+1):
        c = cube_round(cube_lerp(a, b, 1.0/N * i))
        h = cube_to_axial(c)
        results.append((h.q,h.r))
    return results

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

    def hex_corner(self,i):
        angle_deg = 60*i
        return Point(self.center.x+self.size*math.cos(math.radians(angle_deg)),
                     self.center.y+self.size*math.sin(math.radians(angle_deg)))

    def distance_from_center(self):
        x = self.q
        z = self.r
        y = -x-z
        return (abs(x) + abs(y) + abs(z)) / 2

print(cube_linedraw(Hex(-3,3),Hex(3,-2)))

class window(QDialog):

    def __init__(self):
        super(window,self).__init__()
        self.initUI()

    def initUI(self):

        self.iteration   = 0
        self.mouse       = Point(0,0)
        self.redcoords   = Point(0,0)
        self.bluecoords  = Point(0,0)
        self.radius      = 2
        self.polygonsize = 50
        self.windowSize  = Hex(0,0,self.polygonsize).width*(2*self.radius+3.5)
        self.resize(self.windowSize,self.windowSize)
        self.setWindowTitle("PyQt - Hex Board")
        self.center
        self.index = []
        for i in range(-self.radius,self.radius+1):
            for j in range(-self.radius,self.radius+1):
                if (abs(i+j) <= self.radius):
                    self.index.append(Point(i,j))

        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def createPoly(self,item):
        polygon = QPolygonF()
        for i in range(6): # add the points of polygon
            coords = item.hex_corner(i)
            polygon.append(QPointF(self.windowSize/2+coords.x,
                                   self.windowSize/2-2*item.center.y+coords.y))

        return polygon

    def reset(self):
        #don't reset mouse coordinates
        self.redcoords  = Point(0,0)
        self.bluecoords = Point(0,0)
        self.iteration  = 1

    def mousePressEvent(self,QMouseEvent):
        pos = QMouseEvent.pos()
        x   = self.windowSize/2 - QMouseEvent.x()
        y   = self.windowSize/2 - QMouseEvent.y()
        self.mouse = Point(pixel_to_hex(x,y,self.polygonsize).q,
                           pixel_to_hex(x,y,self.polygonsize).r)
        self.iteration+=1
        if self.iteration>3: #reset the board
            self.reset()

        self.update()

    def paintEvent(self, event):
        distance = Hex(self.mouse.x,self.mouse.y).distance_from_center()
        painter  = QPainter(self)
        self.pen = QPen(QColor(0,0,0))                      # set lineColor
        self.pen.setWidth(3)                                # set lineWidth
        painter.setPen(self.pen)
        if self.iteration == 0:
            for item in self.index:
                self.brush = QBrush(QColor(255,255,255,255))
                painter.setBrush(self.brush)
                polygon = self.createPoly(Hex(item.x,item.y,self.polygonsize))
                painter.drawPolygon(polygon)
        elif self.iteration == 1:
            if distance > self.radius: #not valid hex chosen
                for item in self.index:
                    #draw remainder of white hexes
                    self.brush = QBrush(QColor(255,255,255,255))
                    painter.setBrush(self.brush)
                    polygon = self.createPoly(Hex(item.x,item.y,self.polygonsize))
                    painter.drawPolygon(polygon)
                    self.iteration = 0 #reset to redraw red hex
            else: #valid hex choses
                for item in self.index:
                    if (item.x == self.mouse.x and item.y == self.mouse.y):
                        #draw red hex
                        self.redcoords = Point(item.x,item.y)
                        self.brush = QBrush(QColor(255,0,0,255))
                        painter.setBrush(self.brush)
                        polygon = self.createPoly(Hex(item.x,item.y,self.polygonsize))
                        painter.drawPolygon(polygon)
                    else:
                        #draw remainder of white hexes
                        self.brush = QBrush(QColor(255,255,255,255))
                        painter.setBrush(self.brush)
                        polygon = self.createPoly(Hex(item.x,item.y,self.polygonsize))
                        painter.drawPolygon(polygon)
        elif self.iteration == 2:
            if distance > self.radius: #not valid hex chosen
                for item in self.index:
                    if (item.x == self.redcoords.x and item.y == self.redcoords.y):
                        #redraws the old red hex
                        self.brush = QBrush(QColor(255,0,0,255))
                        painter.setBrush(self.brush)
                        polygon = self.createPoly(Hex(item.x,item.y,self.polygonsize))
                        painter.drawPolygon(polygon)
                    else:
                        #draw the remainder white hex
                        self.brush = QBrush(QColor(255,255,255,255))
                        painter.setBrush(self.brush)
                        polygon = self.createPoly(Hex(item.x,item.y,self.polygonsize))
                        painter.drawPolygon(polygon)
                    self.iteration = 1
            else:
                for item in self.index:
                    if (self.mouse.x == self.redcoords.x and self.mouse.y == self.redcoords.y ):
                        #undo red hex
                        self.iteration=0
                        self.brush = QBrush(QColor(255,255,255,255))
                        painter.setBrush(self.brush)
                        polygon = self.createPoly(Hex(item.x,item.y,self.polygonsize))
                        painter.drawPolygon(polygon)
                    elif (item.x == self.mouse.x and item.y == self.mouse.y):
                        #draws blue hex
                        self.bluecoords = Point(item.x,item.y)
                        self.brush = QBrush(QColor(0,0,255,255))
                        painter.setBrush(self.brush)
                        polygon = self.createPoly(Hex(item.x,item.y,self.polygonsize))
                        painter.drawPolygon(polygon)
                    elif (item.x == self.redcoords.x and item.y == self.redcoords.y):
                        #redraws the old red hex
                        self.brush = QBrush(QColor(255,0,0,255))
                        painter.setBrush(self.brush)
                        polygon = self.createPoly(Hex(item.x,item.y,self.polygonsize))
                        painter.drawPolygon(polygon)
                    else:
                        #draw the remainder white hex
                        self.brush = QBrush(QColor(255,255,255,255))
                        painter.setBrush(self.brush)
                        polygon = self.createPoly(Hex(item.x,item.y,self.polygonsize))
                        painter.drawPolygon(polygon)
        elif self.iteration == 3:
            if distance > self.radius: #not valid hex chosen
                for item in self.index:
                    if (item.x == self.redcoords.x and item.y == self.redcoords.y):
                        #redraws the old red hex
                        self.brush = QBrush(QColor(255,0,0,255))
                        painter.setBrush(self.brush)
                        polygon = self.createPoly(Hex(item.x,item.y,self.polygonsize))
                        painter.drawPolygon(polygon)
                    elif (item.x == self.bluecoords.x and item.y == self.bluecoords.y):
                        #draws old blue hex
                        self.bluecoords = Point(item.x,item.y)
                        self.brush = QBrush(QColor(0,0,255,255))
                        painter.setBrush(self.brush)
                        polygon = self.createPoly(Hex(item.x,item.y,self.polygonsize))
                        painter.drawPolygon(polygon)
                    else:
                        #draw the remainder white hex
                        self.brush = QBrush(QColor(255,255,255,255))
                        painter.setBrush(self.brush)
                        polygon = self.createPoly(Hex(item.x,item.y,self.polygonsize))
                        painter.drawPolygon(polygon)
                    self.iteration=2
            else:
                for item in self.index:
                    if (self.mouse.x == self.bluecoords.x and self.mouse.y == self.bluecoords.y ):
                        #undo blue hex
                        self.iteration=1
                        self.brush = QBrush(QColor(255,255,255,255))
                        painter.setBrush(self.brush)
                        polygon = self.createPoly(Hex(item.x,item.y,self.polygonsize))
                        painter.drawPolygon(polygon)
                        if (item.x == self.redcoords.x and item.y == self.redcoords.y):
                            #redraws the old red hex
                            self.brush = QBrush(QColor(255,0,0,255))
                            painter.setBrush(self.brush)
                            polygon = self.createPoly(Hex(item.x,item.y,self.polygonsize))
                            painter.drawPolygon(polygon)
                    else:
                        self.brush = QBrush(QColor(255,255,255,255))
                        painter.setBrush(self.brush)
                        polygon = self.createPoly(Hex(item.x,item.y,self.polygonsize))
                        painter.drawPolygon(polygon)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = window()
    sys.exit(app.exec_())
