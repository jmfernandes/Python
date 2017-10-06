########################################
#
# grades.py
#
# Description: calculates grdes based on breakpoints
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
import bisect
def grade(score, breakpoints=[60,70,80,90], grades ="FDCBA"):
    i = bisect.bisect_right(breakpoints,score)
    return grades[i]

print(grade(60))
glist = [grade(score) for score in [33,99,77,70,69,90,86]]
print(glist)
