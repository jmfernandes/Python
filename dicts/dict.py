########################################
#
# dict.py
#
# Description:
#
#
# Author: Josh Fernandes
#
# Created: Oct 05, 2017
#
# Updated:
#
#
########################################

sizes = ['s', 'm', 'l']
colors= ['black', 'white']
combined = [('s','black'),('m','black'),('l','black'),('s','white'),('m','white'),('l','white')]
combined2 = [[1,['s','black']],[2,['m','black']],[3,['l','black']]]
thing = [[size,color] for color in colors for size in sizes]
thing2 = [(size,color) for size in sizes for color in colors]
thing3 = {size : color for size in sizes for color in colors}
thing4 = {size : color for color in colors for size in sizes}
thing5 = {size : color for size,color in combined2}
thing6 = {size : color for size,color in thing5.items()}
print(thing)
print(thing2)
print(thing3)
print(thing4)
print(thing5)
print(thing5.items())
print(thing5.keys())
print(thing6)
