########################################
#
# functionex.py
#
# Description:
#
#
# Author: Josh Fernandes
#
# Created: Oct 07, 2017
#
# Updated:
#
#
########################################
def factorial(n):
    return 1 if n < 2 else n * factorial(n-1)

def addfunc(a,b):
    return(a,b)

print(factorial(4))
thing = [factorial(n) for n in range(6)]
print(thing)
that = list(map(factorial,range(6)))
print(that)

#get different behavior between list comprehensions verses map function with
#multiple variavbles
xs = [1,2,3]
ys = [6,7,8]
zs = zip(xs,ys)
print(list(zs),'zip list')
print([addfunc(m,n) for m in range(3) for n in range(3)])
print([addfunc(m,n) for m,n in zs ])
print([addfunc(m,n) for m,n in [(3,4),(7.7,9)] ])
print([addfunc(m,m) for m in range(3)])
print(list(map(addfunc,range(3),range(3))))
# print(list(map(addfunc,[0,1,2],[3,4,5,6])))
