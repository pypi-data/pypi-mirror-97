# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool
from . import sale

__all__ = ['register']


def register():
    Pool.register(
        sale.SaleLine,
        module='sale_price_with_tax', type_='model')
