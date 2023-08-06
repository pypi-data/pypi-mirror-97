# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
import unittest


from trytond.tests.test_tryton import ModuleTestCase
from trytond.tests.test_tryton import suite as test_suite


class SalePriceWithTaxTestCase(ModuleTestCase):
    'Test Sale Price With Tax module'
    module = 'sale_price_with_tax'


def suite():
    suite = test_suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
            SalePriceWithTaxTestCase))
    return suite
