# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
import unittest

from decimal import Decimal

from trytond.tests.test_tryton import ModuleTestCase, with_transaction
from trytond.tests.test_tryton import suite as test_suite
from trytond.pool import Pool
from trytond.exceptions import UserError


from trytond.modules.company.tests import create_company, set_company
from trytond.modules.account.tests import create_chart
from trytond.modules.account.tests import test_account


def create_tax(name, parent=None, reverse_charge=True):
    pool = Pool()
    Account = pool.get('account.account')
    Tax = pool.get('account.tax')

    account, = Account.search([
        ('parent', '=', None),
    ])
    tax_account, = Account.search([
        ('name', '=', 'Main Tax'),
    ])
    tax = Tax()
    tax.name = tax.description = name
    tax.type = 'percentage'
    tax.rate = Decimal('0.2')
    tax.parent = parent
    tax.account = account
    tax.invoice_account = tax_account
    tax.credit_note_account = tax_account
    tax.reverse_charge = reverse_charge
    tax.save()
    return tax


class AccountTaxReverseChargeTestCase(ModuleTestCase):
    'Test Account Tax Reverse Charge module'
    module = 'account_tax_reverse_charge'

    @with_transaction()
    def test_0010_checkreversecharge(self):
        '''
        Check if the validation for same setting of all
        taxes in a tree works
        '''
        pool = Pool()
        Tax = pool.get('account.tax')

        company = create_company()
        with set_company(company):
            create_chart(company)

            tax1 = create_tax('Tax1')
            tax2 = create_tax('Tax1_1', parent=tax1)
            tax3 = create_tax('Tax1_2', parent=tax1)
            tax4 = create_tax('Tax2_1', parent=tax2)
            tax5 = create_tax('Tax2_2', parent=tax2)

            with self.assertRaises(UserError):
                create_tax('Tax6', parent=tax3, reverse_charge=False)

            with self.assertRaises(UserError):
                tax5.reverse_charge = False
                tax5.save()

            with self.assertRaises(UserError):
                Tax.write([tax2, tax4, tax5], {
                        'reverse_charge': False,
                        })
            with self.assertRaises(UserError):
                Tax.write([tax1, tax2, tax4, tax5], {
                        'reverse_charge': False,
                        })

            Tax.write([tax1, tax2, tax3, tax4, tax5], {
                    'reverse_charge': False,
                    })


def suite():
    suite = test_suite()
    for test in test_account.suite():
        if test._testMethodName == 'test_update_chart':
            suite.addTest(test)
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
            AccountTaxReverseChargeTestCase))
    return suite
