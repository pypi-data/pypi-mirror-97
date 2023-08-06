# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from . import purchase
from . import move

__all__ =  ['register']


def register():
    Pool.register(
        purchase.PurchaseLine,
        move.Move,
        module='purchase_discount', type_='model')
    Pool.register(
        purchase.PurchaseDiscountReport,
        module='purchase_discount', type_='report')
