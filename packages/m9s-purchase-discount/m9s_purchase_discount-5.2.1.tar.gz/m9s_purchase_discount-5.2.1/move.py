# This file is part of purchase_discount module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import PoolMeta

from .purchase import DIGITS, DISCOUNT_DIGITS


class Move(metaclass=PoolMeta):
    __name__ = 'stock.move'

    @classmethod
    def __setup__(cls):
        super(Move, cls).__setup__()
        cls.unit_price.digits = (20, DIGITS + DISCOUNT_DIGITS)
        # Compatibility with purchase_shipment_cost
        if hasattr(cls, 'unit_shipment_cost'):
            cls.unit_shipment_cost.digits = cls.unit_price.digits
