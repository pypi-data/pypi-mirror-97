# The COPYRIGHT file at the top level of this repository
# contains the full copyright notices and license terms.
import unittest
from decimal import Decimal
import trytond.tests.test_tryton
from trytond.tests.test_tryton import test_view, test_depends
from trytond.tests.test_tryton import POOL, DB_NAME, USER, CONTEXT
from trytond.transaction import Transaction
from trytond.exceptions import UserError


class AccountTaxReverseChargeTestCase(unittest.TestCase):
    'Test AccountTaxReverseCharge module.'

    def setUp(self):
        trytond.tests.test_tryton.install_module('account_tax_reverse_charge')
        self.tax = POOL.get('account.tax')
        self.tax_code = POOL.get('account.tax.code')
        self.account = POOL. get('account.account')
        self.company = POOL.get('company.company')

    def _create_tax(self, name, parent=None, reverse_charge=True):
        account, = self.account.search([
            ('parent', '=', None),
        ])
        tax_account, = self.account.search([
            ('name', '=', 'Main Tax'),
        ])
        tax = self.tax()
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

    def test0005views(self):
        'Test views.'
        test_view('account_tax_reverse_charge')

    def test0006depends(self):
        'Test depends.'
        test_depends()

    def test0010checkreversecharge(self):
        'Test check of tree of taxes for correct reverse charge configuration'
        with Transaction().start(DB_NAME, USER, context=CONTEXT):
            with Transaction().set_user(0):
                tax1 = self._create_tax('Tax1')
                tax2 = self._create_tax('Tax2', parent=tax1)
                tax3 = self._create_tax('Tax3', parent=tax1)
                self._create_tax('Tax4', parent=tax2)
                self._create_tax('Tax5', parent=tax2)

                self.assertRaises(
                    UserError, self._create_tax, 'Tax6', tax3, False)


def suite():
    suite = trytond.tests.test_tryton.suite()
    from trytond.modules.company.tests import test_company
    for test in test_company.suite():
        if test not in suite:
            suite.addTest(test)
    from trytond.modules.account.tests import test_account
    for test in test_account.suite():
        if test._testMethodName == 'test0010account_chart':
            suite.addTest(test)
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        AccountTaxReverseChargeTestCase))
    return suite
