# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
import unittest


from trytond.tests.test_tryton import ModuleTestCase
from trytond.tests.test_tryton import suite as test_suite


class AccountTaxRuleZoneTestCase(ModuleTestCase):
    'Test Account Tax Rule Zone module'
    module = 'account_tax_rule_zone'
    extras = [
        'account_invoice',
        'project_invoice',
        'purchase',
        'purchase_request',
        'sale',
        ]

def suite():
    suite = test_suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
            AccountTaxRuleZoneTestCase))
    return suite
