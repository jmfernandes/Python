########################################
#
# cartesian.py
#
# Description:
#
#
# Author: Josh Fernandes
#
# Created: Sep 13, 2017
#
# Updated:
#
#
########################################
from collections import namedtuple

colors = ['black','white']
sizes = ['S','M','L']
tshirts = [(color,size) for color in colors for size in sizes]
print (tshirts)
othershirts = [(color,size) for size in sizes for color in colors]
print (othershirts)
print(othershirts.__len__())
print(othershirts.__contains__('black'))

##tuples as records
lax_coordinates = (33.9425,-118.408056)
city,year,pop,chg,area = ('Tokyo',2003,32450,0.66,8014)
traveler_ids = [('USA','31195855'), ('BRA','CE34256'),('ESP','XDA205856')]
for passport in sorted(traveler_ids):
    print('%s/%s' % passport)
#unpacking
for country, _ in traveler_ids:
    print(country)

a,b,*rest,c = range(6)
print (a)
print (b)
print (*rest)
print (c)

print('{:15} | {:<19} | {:3^9} | {:>20} | '.format('','lat','long','extra'))

#named tuple
City = namedtuple('City','name country population coordinates')
tokyo = City('Tokyo', 'JP', 36.933, (35.689722,139.691667))
print(tokyo.coordinates)
LatLong = namedtuple('LatLong', 'lat long')
delhi_data = ('Delhi NCR', 'IN', 21.935, LatLong(28.613889,77.208889))
delhi = City(*delhi_data) #City(delhi_data) passes it all as name arugment
print('the population is %s' % (delhi.population))
