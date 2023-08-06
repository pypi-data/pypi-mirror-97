# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
import unittest


from trytond.tests.test_tryton import ModuleTestCase
from trytond.tests.test_tryton import suite as test_suite


class SaleSupplyStateTestCase(ModuleTestCase):
    'Test Sale Supply State module'
    module = 'sale_supply_state'


def suite():
    suite = test_suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
            SaleSupplyStateTestCase))
    return suite
