# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from . import tax

__all__ = ['register']


def register():
    Pool.register(
        tax.Tax,
        tax.TaxTemplate,
        module='account_tax_reverse_charge', type_='model')
