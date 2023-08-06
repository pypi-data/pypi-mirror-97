# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
import unittest


from trytond.tests.test_tryton import ModuleTestCase
from trytond.tests.test_tryton import suite as test_suite


class AccountTaxRecapitulativeStatementTestCase(ModuleTestCase):
    'Test Account Tax Recapitulative Statement module'
    module = 'account_tax_recapitulative_statement'
    extras = ['account_invoice']

def suite():
    suite = test_suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
            AccountTaxRecapitulativeStatementTestCase))
    return suite
