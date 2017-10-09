########################################
#
# strdict.py
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
######S#################################
class StrKeyDict(dict):

    def __missing__(self,key):
        if isinstance(key,str):
            raise KeyError(key)
        return self[str(key)]

    def get(self,key,default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def __contains__(self,key):
        return key in self.keys() or str(key) in self.keys()

d = StrKeyDict([('name', 'josh'),('age',28),('career','physicist')])

print(d["name"])
print(d)
print(d.get('town','blah'))
d['town']='long beach'
print(d)
print(d.__contains__('age'))
