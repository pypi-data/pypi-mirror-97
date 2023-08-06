# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from . import product
from . import sale

__all__ = ['register']


def register():
    Pool.register(
        product.Product,
        product.ProductKitLine,
        product.ProductSupplier,
        sale.Sale,
        sale.SaleLine,
        module='sale_kit', type_='model')
