import sys
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QDialog

def window():
    app = QApplication(sys.argv)
    widget = QDialog()

    buttonOne = QPushButton(widget)
    buttonOne.setText("Button 1")
    buttonOne.move(50,20)
    buttonOne.clicked.connect(b1_clicked)

    buttonTwo = QPushButton(widget)
    buttonTwo.setText("Button 2")
    buttonTwo.move(50,50)
    buttonTwo.clicked.connect(b2_clicked)

    label = QLabel(widget)
    label.setText("Hello World")
    widget.setGeometry(400,100,500,150)
    label.move(250,100)
    widget.setWindowTitle("PyQt")
    widget.show()
    sys.exit(app.exec_())

def b1_clicked():
    print ("Button 1 clicked")

def b2_clicked():
    print ("Button 2 clicked")

if __name__ == '__main__':
    window()
