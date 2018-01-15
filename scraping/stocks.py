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

holdings = {
            'BOTZ': {'shares' : 2, 'sector' : 'technology'},
            'SLIM': {'shares' : 2, 'sector' : 'health'}
            }
print(holdings)
print(holdings['BOTZ'])
print(holdings['BOTZ']['shares'])
print(type(holdings['BOTZ']['shares']))
print(type(holdings['BOTZ']['sector']))
print(holdings.keys())

holdings['CORT'] = {'shares' : 2, 'sector' : 'health'}

for key,value in holdings.items():
    print(key,' - ', value)
