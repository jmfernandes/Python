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
