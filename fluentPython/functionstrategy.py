########################################
#
# functionstrategy.py
#
# Description:
#
#
# Author: Josh Fernandes
#
# Created: Jan 15, 2018
#
# Updated:
#
#
########################################
from collections import namedtuple

Customer = namedtuple('Customer', 'name fidelity')

class LineItem:

    def __init__(self,product, quantity, price):
        self.product = product
        self.quantity = quantity
        self.price = price

    def total(self):
        return self.price * self.quantity

class Order:

    def __init__(self, customer, cart, promotion=None):
        self.customer = customer
        self.cart = list(cart)
        self.promotion = promotion

    def total(self):
        if not hasattr(self, '__total'):
            self.__total = sum(item.total() for item in self.cart)
        return self.__total

    def due(self):
        if self.promotion is None:
            discount = 0
        else:
            discount = self.promotion(self)
        return self.total() - discount

    def __repr__(self):
        fmt = '<Order total: {:.2f} due: {:.2f}>'
        return fmt.format(self.total(),self.due())

def fidelity_promo(order):
    """return 5% dicsount for customer with 1000 fidelity points """
    return order.total() * 0.05 if order.customer.fidelity >= 1000 else 0

def bulk_item_promo(order):
    """10% discount for each LineItem with 20 or more units """
    discount = 0
    for item in order.cart:
        if item.quantity >= 20:
            discount += item.total() * 0.1
    return discount

def large_order_promo(order):
    """ 7% discount for orders with 10 or more distinct items"""
    distinct_items = {item.product for item in order.cart}
    if len(distinct_items) >= 10:
        return order.total() * 0.07
    return 0

promos = [fidelity_promo,bulk_item_promo,large_order_promo]

def best_promo(order):
    """ select the best discount """
    return max(promo(order) for promo in promos)

joe = Customer('John Doe', 0)
ann = Customer('ann smith', 1100)
cart = [LineItem('banana',4,0.5),LineItem('apple',10,1.5),LineItem('watermelon',5,5.0)]
print(Order(ann,cart,fidelity_promo))
print(Order(ann,cart,None))
print(Order(ann,cart,best_promo))
