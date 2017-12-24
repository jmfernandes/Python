import sys
from PyQt5.QtCore import    (
                            QEvent,
                            Qt,
                            QObject
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
                            QDesktopWidget
                            )

from PyQt5.QtGui import     (
                            QFont,
                            QIntValidator,
                            QPalette,
                            QColor,
                            QPainter,
                            QPen
                            )


def federal_tax(income):
    cutoff0 = 0
    cutoff1 = 9225
    cutoff2 = 37450
    cutoff3 = 90750
    rate0 = 0
    rate1 = 0.1
    rate2 = 0.15
    rate3 = 0.25
    rate4 = 0.28
    totaltax0 = (rate0*cutoff0)
    totaltax1 = (rate1*(cutoff1-cutoff0)) + totaltax0
    totaltax2 = (rate2*(cutoff2-cutoff1)) + totaltax1
    totaltax3 = (rate3*(cutoff3-cutoff2)) + totaltax2
    if (income < cutoff1 ):
        outcome = ((income - cutoff0) * rate1) + totaltax0
    elif (income < cutoff2):
        outcome = ((income - cutoff1) * rate2) + totaltax1
    elif (income < cutoff3):
        outcome = ((income - cutoff2) * rate3) + totaltax2
    else:
        outcome = ((income - cutoff3) * rate4) + totaltax3

    return("{0:.2f}".format(outcome))

def state_tax(income):
    cutoff0 = 0
    cutoff1 = 7850
    cutoff2 = 18610
    cutoff3 = 29372
    cutoff4 = 40773
    cutoff5 = 51530
    rate0 = 0
    rate1 = 0.01
    rate2 = 0.02
    rate3 = 0.04
    rate4 = 0.06
    rate5 = 0.08
    rate6 = 0.093
    totaltax0 = (rate0*cutoff0)
    totaltax1 = (rate1*(cutoff1-cutoff0)) + totaltax0
    totaltax2 = (rate2*(cutoff2-cutoff1)) + totaltax1
    totaltax3 = (rate3*(cutoff3-cutoff2)) + totaltax2
    totaltax4 = (rate4*(cutoff4-cutoff3)) + totaltax3
    totaltax5 = (rate5*(cutoff5-cutoff4)) + totaltax4
    if (income < cutoff1 ):
        outcome = ((income - cutoff0) * rate1) + totaltax0
    elif (income < cutoff2):
        outcome = ((income - cutoff1) * rate2) + totaltax1
    elif (income < cutoff3):
        outcome = ((income - cutoff2) * rate3) + totaltax2
    elif (income < cutoff4):
        outcome = ((income - cutoff3) * rate4) + totaltax3
    elif (income < cutoff5):
        outcome = ((income - cutoff4) * rate5) + totaltax4
    else:
        outcome = ((income - cutoff5) * rate6) + totaltax5

    return("{0:.2f}".format(outcome))

class MainApp(QWidget):

    def __init__(self):
        super().__init__()
        #initialize top level values that never change
        self.title  = 'Finance'
        self.left   = 10
        self.top    = 10
        self.width  = 320
        self.height = 400

        self.initUI()


    def initUI(self): #run funciton that creates all visual elements

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.IncomeTitle    = QLabel('Income')
        self.MonthlyTitle    = QLabel('Monthly Budget')
        self.TaxableTitle   = QLabel('Taxable Income')
        self.FedTaxTitle    = QLabel('Federal Income Tax')
        self.StateTaxTitle  = QLabel('State Income Tax')
        self.SocialTaxTitle = QLabel('Social Security Tax')
        self.TotalTaxTitle  = QLabel('Total Tax')

        self.IncomeEdit = QLineEdit()
        self.MonthlyEdit = QLineEdit()
        self.TaxableEdit = QLineEdit()
        self.FedTaxEdit = QLineEdit()
        self.StateTaxEdit = QLineEdit()
        self.SocialTaxEdit = QLineEdit()
        self.TotalTaxEdit = QLineEdit()
        self.TaxableEdit.setReadOnly(True)
        self.FedTaxEdit.setReadOnly(True)
        self.StateTaxEdit.setReadOnly(True)
        self.SocialTaxEdit.setReadOnly(True)
        # lcd = QLCDNumber(self)

        self.onlyInt = QIntValidator()
        self.IncomeEdit.setValidator(self.onlyInt)

        self.grid = QGridLayout()
        self.paddingspace = 10
        self.grid.setSpacing(self.paddingspace)

        #set palette color
        self.palette = QPalette()

        self.grid.addWidget(self.IncomeTitle,   0, 0)
        self.grid.addWidget(self.IncomeEdit,    1, 0)
        self.grid.addWidget(self.TaxableTitle,  2, 0)
        self.grid.addWidget(self.TaxableEdit,   3, 0)
        self.grid.addWidget(self.FedTaxTitle,   4, 0)
        self.grid.addWidget(self.FedTaxEdit,    5, 0)
        self.grid.addWidget(self.StateTaxTitle, 6, 0)
        self.grid.addWidget(self.StateTaxEdit,  7, 0)
        self.grid.addWidget(self.SocialTaxTitle,8, 0)
        self.grid.addWidget(self.SocialTaxEdit, 9, 0)
        self.grid.addWidget(self.TotalTaxTitle, 10, 0)
        self.grid.addWidget(self.TotalTaxEdit,  11, 0)
        self.grid.addWidget(self.MonthlyTitle,   12, 0)
        self.grid.addWidget(self.MonthlyEdit,    13, 0)


        ##
        r1 = QRadioButton("Single")
        r2 = QRadioButton("Married")
        self.grid.addWidget(r1, 1, 1)
        self.grid.addWidget(r2, 1, 2)
        r1.setChecked(True)
        self.bg = QButtonGroup(self)
        self.bg.addButton(r1,1)
        self.bg.addButton(r2,2)

        # bg.buttonToggled.connect(self.on_radio_button_toggled)
        # bg.buttonClicked['QAbstractButton *'].connect(self.button_clicked)
        self.bg.buttonClicked.connect(self.update)

        #connect to update function
        self.IncomeEdit.textEdited.connect(self.update)
        self.TotalTaxEdit.textChanged.connect(self.budget)

        #zero out values


        self.setLayout(self.grid)
        self.show()

    def budget(self):
        print('budget')

    def update(self):
        # print(self.bg.checkedId())
        if(len(self.IncomeEdit.text()) != 0): #only run if there are values
            number = int(self.IncomeEdit.text())
            if (self.bg.checkedId() == 1):
                standard_deduction = 6300
            else:
                standard_deduction = 12000
            self.TaxableEdit.setText(str(max(0,number-standard_deduction)))
            self.FedTaxEdit.setText(str(federal_tax(int(self.TaxableEdit.text()))))
            self.StateTaxEdit.setText(str(state_tax(int(self.IncomeEdit.text()))))
            self.SocialTaxEdit.setText(str("{0:.2f}".format(int(self.IncomeEdit.text())*0.0765)))
            self.TotalTaxEdit.setText(str("{0:.2f}".format(float(self.FedTaxEdit.text())+float(self.StateTaxEdit.text())+float(self.SocialTaxEdit.text()))))
            difference = float(self.IncomeEdit.text()) - float(self.TotalTaxEdit.text())
            divide_str = str("{0:.2f}".format(difference / 12.0))
            self.MonthlyEdit.setText(divide_str)
            if (difference/12.0 < 3000):
                # self.palette.setColor(self.backgroundRole(), QColor('red'))
                # self.MonthlyEdit.setPalette(self.palette)
                self.MonthlyEdit.setStyleSheet("QLineEdit { background-color : red; color : black; }")
            else:
                # self.palette.setColor(self.backgroundRole(), QColor('blue'))
                # self.MonthlyEdit.setPalette(self.palette)
                self.MonthlyEdit.setStyleSheet("QLineEdit { background-color : green; color : black; }")


    # def paintEvent(self, e):
    #
    #     qp = QPainter()
    #     qp.begin(self)
    #     self.drawLines(qp)
    #     qp.end()

    # def drawLines(self, qp):
    #
    #     pen = QPen(Qt.black, 2, Qt.SolidLine)
    #
    #     qr = self.frameGeometry()
    #     qo = self.frameGeometry()
    #     print(qr.height())
    #     # print(qo.height())
    #     rows = qr.height() /(self.grid.rowCount()-1)
    #     width = qr.width()
    #     padding = self.paddingspace / 2
    #     row_draw = rows * 2 + 5
    #     qp.setPen(pen)
    #     qp.drawLine(20, row_draw, width-20, row_draw)
    #
    #     pen.setStyle(Qt.DashLine)
    #
    #     # row_draw = rows * 1
    #     # qp.setPen(pen)
    #     # qp.drawLine(20, row_draw, width-20, row_draw)
    #
    #     row_draw = rows * 9 + 10
    #     qp.setPen(pen)
    #     qp.drawLine(20, row_draw, width-20, row_draw)



    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()



if __name__ == '__main__':

    app = QApplication(sys.argv)
    main = MainApp()
    sys.exit(app.exec_())
