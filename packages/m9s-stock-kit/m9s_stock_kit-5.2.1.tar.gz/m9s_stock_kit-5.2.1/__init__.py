# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from . import product
from . import inventory

__all__ = ['register']


def register():
    Pool.register(
        product.Template,
        product.Product,
        inventory.InventoryLine,
        module='stock_kit', type_='model')
