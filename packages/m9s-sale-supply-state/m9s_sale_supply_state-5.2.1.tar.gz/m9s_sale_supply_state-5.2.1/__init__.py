# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from . import sale

__all__ = ['register']


def register():
    Pool.register(
        sale.Sale,
        module='sale_supply_state', type_='model')
