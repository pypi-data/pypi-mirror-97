# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

from trytond.pool import Pool
from . import product

__all__ = ['register']


def register():
    Pool.register(
        product.ProductAttributeSet,
        product.ProductAttribute,
        product.ProductAttributeSelectionOption,
        product.ProductAttributeAttributeSet,
        product.Template,
        product.ProductProductAttribute,
        product.Product,
        module='product_attribute_strict', type_='model')
