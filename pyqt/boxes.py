import sys
from PyQt5 import QtGui, QtCore,QtWidgets


class cell(object):
    def __init__(self, c, x, y, w, h):
        self.color = c
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def drawRectangles(self, qp):
        qp.setBrush(self.color)
        qp.drawRect(self.x, self.y, self.w, self.h)


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(50, 50, 1000, 800)
        self.setWindowTitle("PyQT tuts!")
        self.cells = []

        now = QtCore.QTime.currentTime()
        QtCore.qsrand(now.msec())
        self.createCells()

    def createCells(self):
        for i in range(100):
            self.cells.append(cell(QtGui.QColor(QtCore.qrand() % 256,
                                                QtCore.qrand() % 256,
                                                QtCore.qrand() % 256),
                                   QtCore.qrand() % self.width(), QtCore.qrand() % self.height(),
                                   QtCore.qrand() % 40, QtCore.qrand() % 40))
        self.update()

    def paintEvent(self, e):
        qp = QtGui.QPainter(self)
        for c in self.cells:
            c.drawRectangles(qp)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
