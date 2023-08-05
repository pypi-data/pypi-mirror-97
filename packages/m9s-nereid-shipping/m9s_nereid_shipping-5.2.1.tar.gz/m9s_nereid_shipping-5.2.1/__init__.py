# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool
from . import checkout
from . import website

__all__ = ['register']


def register():
    Pool.register(
        checkout.Cart,
        checkout.Checkout,
        website.Website,
        website.WebsiteCarrier,
        module='nereid_shipping', type_='model')
