########################################
#
# functions.py
#
# Description:
#
#
# Author: Josh Fernandes
#
# Created: Jan 09, 2018
#
# Updated:
#
#
########################################

def factorial(n):
    '''returns n!'''
    return 1 if n < 2 else n * factorial(n-1)

print(factorial(42))
print(factorial.__doc__)
print(type(factorial))
