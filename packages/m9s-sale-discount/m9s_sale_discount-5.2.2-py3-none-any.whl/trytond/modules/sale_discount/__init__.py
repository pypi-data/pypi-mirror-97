# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from . import sale
from . import move

__all__ = ['register']


def register():
    Pool.register(
        sale.Sale,
        sale.SaleLine,
        move.Move,
        module='sale_discount', type_='model')
    Pool.register(
        sale.SaleReport,
        module='sale_discount', type_='report')
