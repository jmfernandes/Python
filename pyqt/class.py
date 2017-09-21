import sys
from PyQt5.QtCore import QObject
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QToolTip, QWidget, QLabel, QPushButton, QDialog

class window(QDialog):

    def __init__(self):
        super(window,self).__init__()
        self.initUI()

    def initUI(self):
        buttonOne = QPushButton(self)
        buttonOne.setText("Button 1")
        buttonOne.move(50,20)
        buttonOne.clicked.connect(self.b1_clicked)

        buttonTwo = QPushButton(self)
        buttonTwo.setText("Button 2")
        buttonTwo.setToolTip('This is a <b>QPushButton</b> widget')
        buttonTwo.resize(buttonTwo.sizeHint())
        buttonTwo.move(50,50)
        buttonTwo.clicked.connect(self.b2_clicked)

        QToolTip.setFont(QFont('SansSerif', 10))
        self.setToolTip('This is a <b>QWidget</b> widget')

        label = QLabel(self)
        label.setText("Hello World")
        label.move(250,100)

        self.resize(500,150)
        self.center
        self.setWindowTitle("PyQt")
        self.show()

    def b1_clicked(self):
        print ("Button 1 clicked")

    def b2_clicked(self):
        print ("Button 2 clicked")

    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = window()
    sys.exit(app.exec_())
