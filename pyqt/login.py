import sys
import requests
from PyQt5.QtCore import    (
                            QRegExp,
                            QTimer
                            )
from PyQt5.QtGui import     (
                            QRegExpValidator,
                            QColor,
                            QIcon
                            )
from PyQt5.QtWidgets import (
                            QWidget,
                            QDialog,
                            QMainWindow,
                            QApplication,
                            QFormLayout,
                            QLineEdit,
                            QLabel,
                            QPushButton,
                            QMessageBox,
                            QCheckBox,
                            QTextBrowser,
                            QHBoxLayout,
                            QVBoxLayout,
                            QTableWidget,
                            QStatusBar,
                            QAction,
                            QMenu,
                            QTableWidgetItem
                            )

# from mainwindow import Ui_MainWindow
session = requests.Session()
session.headers = {
"Accept": "*/*",
"Accept-Encoding": "gzip,defalte",
"Accept-Language": "en;q=1",
"Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
"X-Robinhood-API-Version": "1.0.0",
"Connection": "keep-alive",
"User-Agent": "Robinhood/823 (iphone; iOS 7.1.2, Scale/2.00)"
}

def get_quote(symbols,info=None):
    if isinstance(symbols,str):
        try:
            symbols = ast.literal_eval(symbols)
        except:
            symbols = [symbols]

    quoteurl = 'https://api.robinhood.com/quotes/?symbols='

    for i,s in enumerate(symbols):
        if len(symbols) == 1 or i == len(symbols)-1:
            quoteurl += s.upper()
        else:
            quoteurl += s.upper() + ','

    res = session.get(quoteurl)
    res_data = res.json()

    assert None not in res_data['results'], "One of the Ticker symbols is wrong"

    if info:
        give_data = []
        assert info in res_data['results'][0], "NOT a valid parameter in results"
        for value in res_data['results']:
            give_data.append(value[info])
        return(give_data)
    else:
        return(res_data['results'])

def get_latest_price(symbols):
    if isinstance(symbols,str):
        try:
            symbols = ast.literal_eval(symbols)
        except:
            symbols = [symbols]

    myquote = get_quote(symbols,info='last_extended_hours_trade_price')
    price_list = []
    i = 0
    for quote in myquote:
        if quote == None:
            quote = get_quote(symbols[i],info='last_trade_price')[0]
        price_list.append(quote)
        i += 1
    return(price_list)

username = ''

def get_latest_price(symbols):
    if isinstance(symbols,str):
        try:
            symbols = ast.literal_eval(symbols)
        except:
            symbols = [symbols]

    myquote = get_quote(symbols,info='last_extended_hours_trade_price')
    price_list = []
    i = 0
    for quote in myquote:
        if quote == None:
            quote = get_quote(symbols[i],info='last_trade_price')[0]
        price_list.append(quote)
        i += 1
    return(price_list)

def build_holdings():
    holdings = {}
    positions_data = session.get('https://api.robinhood.com/positions/?nonzero=true').json()

    portfolios_data = session.get('https://api.robinhood.com/portfolios/').json()['results'][0]
    if portfolios_data['extended_hours_equity'] is not None:
        equity = max(float(portfolios_data['equity']),float(portfolios_data['extended_hours_equity']))
    else:
        equity = float(portfolios_data['equity'])

    accounts_data = session.get('https://api.robinhood.com/accounts/').json()
    cash = "{0:.2f}".format(float(accounts_data['results'][0]['cash'])+float(accounts_data['results'][0]['uncleared_deposits']))

    for item in positions_data['results']:
        instrument_data = session.get(item['instrument']).json()
        symbol = instrument_data['symbol']
        price = get_latest_price(instrument_data['symbol'])[0]
        quantity = item['quantity']
        equity_change = (float(quantity)*float(price))-(float(quantity)*float(item['average_buy_price']))
        fundamental_data = session.get('https://api.robinhood.com/fundamentals/'+symbol+'/').json()
        holdings[symbol]=({'price': price })
        holdings[symbol].update({'quantity': quantity})
        holdings[symbol].update({'average_buy_price': item['average_buy_price']})
        holdings[symbol].update({'equity':"{0:.2f}".format(float(item['quantity'])*float(price))})
        holdings[symbol].update({'percent_change': "{0:.2f}".format((float(price)-float(item['average_buy_price']))*100/float(item['average_buy_price']))})
        holdings[symbol].update({'equity_change':"{0:2f}".format(equity_change)})
        holdings[symbol].update({'type': instrument_data['type']})
        holdings[symbol].update({'simple_name': instrument_data['simple_name']})
        holdings[symbol].update({'id': instrument_data['id']})
        holdings[symbol].update({'pe_ratio': fundamental_data['pe_ratio'] })
        percentage = "{0:.2f}".format(float(item['quantity'])*float(price)*100/(float(equity)-float(cash)))
        holdings[symbol].update({'percentage': percentage})

    return holdings

def build_user_profile():
    user = {}

    res = session.get('https://api.robinhood.com/portfolios/')
    res_data = res.json()
    user['equity'] = res_data['results'][0]['equity']
    user['extended_hours_equity'] = res_data['results'][0]['extended_hours_equity']

    res = session.get('https://api.robinhood.com/accounts/')
    res_data = res.json()
    cash = "{0:.2f}".format(float(res_data['results'][0]['cash'])+float(res_data['results'][0]['uncleared_deposits']))
    user['cash'] = cash

    res = session.get('https://api.robinhood.com/dividends/')
    res_data = res.json()
    dividend_total = 0
    for item in res_data['results']:
        dividend_total += float(item['amount'])
    user['dividend_total'] = "{0:.2f}".format(dividend_total)

    return user

holdings = {}

user = {}

class Login(QDialog):
    def __init__(self, parent=None):
        super(Login, self).__init__(parent)
        self.textName = QLineEdit(self)
        self.textPass = QLineEdit(self)
        form_width=180
        self.stuff = 'hi'
        self.textName.setFixedWidth(form_width)
        self.textPass.setFixedWidth(form_width)

        self.robinhoodtitle = QLabel('                Enter Robinhood Login                ')
        self.usernametitle = QLabel('Email:')
        self.passwordtitle = QLabel('Password:')

        self.buttonLogin = QPushButton('Login', self)
        self.buttonLogin.clicked.connect(self.handleLogin)

        self.layout = QFormLayout(self)
        self.layout.addRow(self.robinhoodtitle)
        self.layout.addRow(QLabel(' '))
        self.layout.addRow(self.usernametitle,self.textName)
        self.layout.addRow(self.passwordtitle,self.textPass)
        self.layout.addRow(self.buttonLogin)

        self.reg_ex = QRegExp('[^@]+@[^@]+\.[^@]+')
        self.username_validator = QRegExpValidator(self.reg_ex, self.textName)
        self.textName.setValidator(self.username_validator)

        self.setFixedSize(self.minimumSizeHint())

    def handleLogin(self):
        payload = {
        'username': self.textName.text(),
        'password': self.textPass.text()
        }
        try:
            res_login = session.post('https://api.robinhood.com/api-token-auth/',data=payload)
            res_login.raise_for_status()
            login_data = res_login.json()
            session.headers['Authorization'] = 'Token ' + login_data['token']
            global username
            username = self.textName.text()
            self.accept()
        except requests.exceptions.HTTPError:
            QMessageBox.warning(
                self, 'Error', 'Bad user or password')

class Window(QMainWindow):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        global holdings
        holdings = build_holdings()
        global user
        user = build_user_profile()
        self.createUI()

    def createUI(self):
        self.setWindowTitle('RobinHood Portfolio')
        #create menubar


        #create status bar
        statusBar = self.statusBar()
        statusBar.showMessage(self.tr("Signed in as "+username))

        #main content
        self.rw = DataWidget()
        self.setCentralWidget(self.rw)

        self.setGeometry(100,100,750,550)


class DataWidget(QWidget):
    def __init__(self, *args):
        QWidget.__init__(self, *args)
        # self.cbUsers = QCheckBox("Hide SYSTEM users")
        # self.cbSorting = QCheckBox("Sorting enabled")

        self.table = TableData()

        self.buttonRefresh = QPushButton('Refesh', self)
        self.buttonRefresh.clicked.connect(self.update_data)


        total_equity_change = 0
        for key,item in holdings.items():
            total_equity_change += float(item['equity_change'])
        total_equity_change += float(user['dividend_total'])

        # AAPL_price = get_latest_price('AAPL')[0]
        self.equitytitle = QLabel('Total Equity:')
        self.equityvaluetitle = QLabel(str("{0:.2f}".format(float(user['equity']))))

        self.initialtitle = QLabel('Initial Investment:')
        self.initialvaluetitle = QLabel(str("{0:.2f}".format(float(user['equity'])-total_equity_change)))

        self.changetitle = QLabel('Total Change:')
        self.changevaluetitle = QLabel(str("{0:.2f}".format(total_equity_change)))

        self.percenttitle = QLabel('Percent Change:')
        self.percentvaluetitle = QLabel(str("{0:.2f}".format(total_equity_change/(float(user['equity'])-total_equity_change))))

        self.textbrowser = QTextBrowser()
        self.textbrowser.setFontFamily("Courier")
        self.textbrowser.setFontPointSize(10)
        hlayout = QHBoxLayout()
        # hlayout.addWidget(self.cbUsers)
        # hlayout.addWidget(self.cbSorting)

        vlayout = QVBoxLayout()
        hlayout.addWidget(self.equitytitle)
        hlayout.addWidget(self.equityvaluetitle)
        hlayout.addWidget(self.initialtitle)
        hlayout.addWidget(self.initialvaluetitle)
        hlayout.addWidget(self.changetitle)
        hlayout.addWidget(self.changevaluetitle)
        hlayout.addWidget(self.percenttitle)
        hlayout.addWidget(self.percentvaluetitle)
        vlayout.addLayout(hlayout)
        vlayout.addWidget(self.buttonRefresh)
        vlayout.addWidget(self.table)

        self.table.display_data('data')
        self.table.show()

        self.setLayout(vlayout)
        self.setGeometry(100,100,750,550)

    def update_label(self):
        total_equity_change = 0
        for key,item in holdings.items():
            total_equity_change += float(item['equity_change'])
        total_equity_change += float(user['dividend_total'])
        self.equityvaluetitle.setText(str("{0:.2f}".format(float(user['equity']))))
        self.initialvaluetitle.setText(str("{0:.2f}".format(float(user['equity'])-total_equity_change)))
        self.changevaluetitle.setText(str("{0:.2f}".format(total_equity_change)))
        self.percentvaluetitle.setText(str("{0:.2f}".format(total_equity_change/(float(user['equity'])-total_equity_change))))

    def update_data(self):
        global holdings
        holdings = build_holdings()
        global user
        user = build_user_profile()
        self.table.display_data('data')
        self.table.show()
        self.update_label()


class TableData(QTableWidget):
    def __init__(self,*args):
        # initiate table
        QTableWidget.__init__(self,*args)
        self.setWindowTitle("QTableWidget")
        # self.resize(800, 550)
        # self.setGeometry(0,0,750,550)
        self.setRowCount(len(holdings))
        self.setColumnCount(6)
        self.setShowGrid(True)

    def display_data(self,data):
        # set label
        rowlabel = []
        for key in holdings:
            rowlabel.append(key)
        columnlabel= ['quantity','price','equity','percent_change','equity_change','percentage']
        self.setHorizontalHeaderLabels(columnlabel)
        self.setVerticalHeaderLabels(rowlabel)

        # set data
        for i,name in enumerate(rowlabel):
            for j,value in enumerate(columnlabel):
                self.setItem(i,j, QTableWidgetItem(holdings[name][value]))
                if (value == 'percent_change' or value == 'equity_change') and float(holdings[name][value]) < 0 :
                    self.item(i, j).setBackground(QColor(255,0,0,150))
                elif (value == 'percent_change' or value == 'equity_change') and float(holdings[name]['percent_change']) < 2 :
                    self.item(i, j).setBackground(QColor(255,255,0,150))
                elif (value == 'percent_change' or value == 'equity_change'):
                    self.item(i, j).setBackground(QColor(0,255,0,150))
if __name__ == '__main__':

    app = QApplication(sys.argv)
    login = Login()

    if login.exec_() == QDialog.Accepted:
        window = Window()
        window.show()
        sys.exit(app.exec_())
