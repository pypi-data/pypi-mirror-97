# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
import unittest


from trytond.tests.test_tryton import ModuleTestCase
from trytond.tests.test_tryton import suite as test_suite


class StockUpdatePlannedDateTestCase(ModuleTestCase):
    'Test Stock Update Planned Date module'
    module = 'stock_update_planned_date'


def suite():
    suite = test_suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
            StockUpdatePlannedDateTestCase))
    return suite
