# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool
from .customs import *
from .product import *

__all__ = ['register']


def register():
    Pool.register(
        TariffCode,
        DutyRate,
        Category,
        Template,
        Product_TariffCode,
        Product,
        module='customs', type_='model')
