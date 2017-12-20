import sys
from PyQt5.QtWidgets import (QWidget,
                            QToolTip,
                            QPushButton,
                            QLineEdit,
                            QLabel,
                            QGridLayout,
                            QLCDNumber,
                            QApplication)
from PyQt5.QtGui import QFont, QIntValidator
from PyQt5.QtCore import QEvent, Qt

class MainApp(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Finance'
        self.left = 10
        self.top = 10
        self.width = 320
        self.height = 100

        self.initUI()


    def initUI(self):

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.IncomeTitle = QLabel('Income')
        self.OutputTitle = QLabel('Output')

        self.IncomeEdit = QLineEdit()
        self.OutputEdit = QLineEdit()
        lcd = QLCDNumber(self)

        self.onlyInt = QIntValidator()
        self.IncomeEdit.setValidator(self.onlyInt)

        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(self.IncomeTitle, 0, 0)
        grid.addWidget(self.IncomeEdit, 1, 0)
        grid.addWidget(self.OutputTitle, 2, 0)
        grid.addWidget(self.OutputEdit, 3, 0)
        grid.addWidget(lcd, 4, 0)

        #connect to update function
        self.IncomeEdit.textEdited.connect(self.update)

        #zero out values


        self.setLayout(grid)
        self.show()

    def update(self):
        if(len(self.IncomeEdit.text()) != 0): #only run if there are values 
            divide_math = int(self.IncomeEdit.text()) / 10.0
            divide_str = str(divide_math)
            self.OutputEdit.setText(divide_str)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()



if __name__ == '__main__':

    app = QApplication(sys.argv)
    main = MainApp()
    sys.exit(app.exec_())
