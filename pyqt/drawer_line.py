import sys
from PyQt5.QtCore import    (
                            QEvent,
                            Qt,
                            QObject,
                            QPoint,
                            pyqtSignal,
                            QSize
                            )

from PyQt5.QtWidgets import (
                            QWidget,
                            QToolTip,
                            QPushButton,
                            QLineEdit,
                            QLabel,
                            QGridLayout,
                            QLCDNumber,
                            QApplication,
                            QRadioButton,
                            QButtonGroup,
                            QAbstractButton,
                            QDesktopWidget,
                            QVBoxLayout
                            )

from PyQt5.QtGui import     (
                            QFont,
                            QIntValidator,
                            QDoubleValidator,
                            QPalette,
                            QColor,
                            QPainter,
                            QPen,
                            QPainterPath
                            )

class Drawer(QWidget):
    newPoint = pyqtSignal(QPoint)
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.x = 0
        self.y = 0
        self.x2=0
        self.y2=0

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawLine(self.x,self.y,self.x2,self.y2)

    def mousePressEvent(self, event):
        self.x = event.x()
        self.y = event.y()

    def mouseReleaseEvent(self, event):
        self.x2 = event.x()
        self.y2 = event.y()
        self.update()

    def mouseMoveEvent(self, event):
        self.newPoint.emit(event.pos())
        self.x2 = event.x()
        self.y2 = event.y()
        self.update()

    def sizeHint(self):
        return QSize(400, 400)

class MyWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setLayout(QVBoxLayout())
        label = QLabel(self)
        drawer = Drawer(self)
        drawer.newPoint.connect(lambda p: label.setText('Coordinates: ( %d : %d )' % (p.x(), p.y())))
        self.layout().addWidget(label)
        self.layout().addWidget(drawer)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MyWidget()
    w.show()
    sys.exit(app.exec_())
