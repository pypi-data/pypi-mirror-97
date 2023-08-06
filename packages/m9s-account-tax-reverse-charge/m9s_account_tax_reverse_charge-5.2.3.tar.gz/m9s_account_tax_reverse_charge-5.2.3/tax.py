# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta
from trytond.exceptions import UserError
from trytond.i18n import gettext


class TaxTemplate(metaclass=PoolMeta):
    __name__ = 'account.tax.template'

    reverse_charge = fields.Boolean('Reverse Charge')

    def _get_tax_value(self, tax=None):
        res = super(TaxTemplate, self)._get_tax_value(tax=tax)
        if not tax or tax.reverse_charge != self.reverse_charge:
            res['reverse_charge'] = self.reverse_charge
        return res


class Tax(metaclass=PoolMeta):
    __name__ = 'account.tax'

    reverse_charge = fields.Boolean('Reverse Charge')

    @classmethod
    def validate(cls, taxes):
        super(Tax, cls).validate(taxes)
        for tax in taxes:
            tax.check_reverse_charge()

    def check_reverse_charge(self):
        taxes = None
        if self.parent:
            taxes = self.search([
                    ('reverse_charge', '!=', self.reverse_charge),
                    ('parent', 'child_of', self.parent.id)
                    ])
        if taxes:
            raise UserError(gettext(
                    'account_tax_reverse_charge.same_reverse_charge',
                    first=self.rec_name, second=taxes[0].rec_name))
