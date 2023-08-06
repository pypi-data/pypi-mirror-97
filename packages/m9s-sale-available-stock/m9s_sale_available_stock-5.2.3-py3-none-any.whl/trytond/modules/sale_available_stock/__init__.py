# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool
from . import sale
from . import stock

__all__ = ['register']


def register():
    Pool.register(
        sale.SaleLine,
        stock.Move,
        module='sale_available_stock', type_='model')
