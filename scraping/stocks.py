########################################
#
# stocks.py
#
# Description:
#
#
# Author: Josh Fernandes
#
# Created: Jan 10, 2018
#
# Updated:
#
#
########################################
import requests
from bs4 import BeautifulSoup

holdings = {
            'BOTZ': {'shares' : 3, 'sector' : 'technology'},
            'ARKK': {'shares' : 3, 'sector' : 'technology'},
            'SLIM': {'shares' : 2, 'sector' : 'health'},
            'PFE': {'shares' : 2, 'sector' : 'health'},
            'CORT': {'shares' : 2, 'sector' : 'health'},
            'BCO': {'shares' : 2, 'sector' : 'financial'},
            'KEM': {'shares' : 4, 'sector' : 'technology'},
            }

website = 'https://finance.yahoo.com/quote/BOTZ?p=BOTZ'
w = 'https://finance.yahoo.com/quote/AAPL?p=AAPL'

result = requests.get(w)
content = result.content
bsObj = BeautifulSoup(content,"html.parser")
sample = bsObj.find("span", {"data-reactid": "14"})
##14 is price #17 is daily change #20 is open price
##

# children = sample.findChildren()
# for child in children:
#     print(child.encode())
#     print("------------")
# super_child = children.find("div",{"data-reactid":"25"})
print(bsObj.h1)
print(sample.get_text())

#update all the holdings
for ticker in holdings:
    print(ticker)
    website = 'https://finance.yahoo.com/quote/'+ticker+'?p='+ticker
    result = requests.get(website)
    content = result.content
    bsObj = BeautifulSoup(content,"html.parser")
    price = bsObj.find("span", {"data-reactid": "14"}).get_text()
    print(price)
    holdings[ticker].update({'price':float(price)})

print(holdings)
# for item in sample:
#     print(item.encode())
#     print('----------------')

# for child in bsObj.find("", {"data-reactid":"35"}, recursive=True).children:
#     print(child)

# print(super_child)
#quote-header-info > div.Mt\(6px\).smartphone_Mt\(15px\) > div.D\(ib\).Maw\(65\%\).Maw\(70\%\)--tab768.Ov\(h\) > div > span.Trsdu\(0\.3s\).Fw\(b\).Fz\(36px\).Mb\(-4px\).D\(ib\)
# print(holdings)
# print(holdings['BOTZ'])
# print(holdings['BOTZ']['shares'])
# print(type(holdings['BOTZ']['shares']))
# print(type(holdings['BOTZ']['sector']))
# print(holdings.keys())

# holdings['CORT'] = {'shares' : 2, 'sector' : 'health'}
# holdings['CORT'].update({'price':30.00})
#
# for key,value in holdings.items():
#     print(key,' - ', value)
