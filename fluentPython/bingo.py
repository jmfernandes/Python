########################################
#
# bingo.py
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

import random

class BingoCage:

    def __init__(self, items):
        self._items = list(items)
        random.shuffle(self._items)

    def pick(self):
        try:
            return self._items.pop()
        except IndexError:
            raise LookupError('pick from empty BingoCage')

    def __call__(self):
        return self.pick()

bingo = BingoCage(range(3))

bingo.pick()
bingo()
bingo()
bingo()
