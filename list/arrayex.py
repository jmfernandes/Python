########################################
#
# array.py
#
# Description: creates large arrray and saves and reads it
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
import array
import random
import time
import numpy

initial = time.time()
# print("%.2f seconds" % (time.time() - initial))
floats = array.array('d', (random.random() for i in range(10**7)))
# print(floats[-1])
print("build array after %.2f seconds" % (time.time() - initial))
update = time.time()
fp = open('floats.bin', 'wb')
floats.tofile(fp) #tofile is array specific method funciton
fp.close()
print("write to file after %.2f seconds" % (time.time() - update))
update = time.time()
floats2 = array.array('d')
# print(floats2)
fp = open('floats.bin','rb')
floats2.fromfile(fp,10**7)
fp.close()
print("read file after %.2f seconds" % (time.time() - update))
update = time.time()
# print(floats2)
# print(floats2[-1])
floats3 = array.array(floats2.typecode,sorted(floats2))
# print(floats3[-1])
print("sort array after %.2f seconds" % (time.time() - update))
update = time.time()
floats4 = numpy.sort(floats2)
print("numpy sort array after %.2f seconds" % (time.time() - update))
