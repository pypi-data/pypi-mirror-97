# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

try:
    from trytond.modules.account_tax_reverse_charge.tests.test_account_tax_reverse_charge import suite
except ImportError:
    from .test_account_tax_reverse_charge import suite

__all__ = ['suite']
