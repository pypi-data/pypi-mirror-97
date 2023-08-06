# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
import unittest


from trytond.tests.test_tryton import ModuleTestCase
from trytond.tests.test_tryton import suite as test_suite


class SaleChannelPaymentGatewayTestCase(ModuleTestCase):
    'Test Sale Channel Payment Gateway module'
    module = 'sale_channel_payment_gateway'


def suite():
    suite = test_suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
            SaleChannelPaymentGatewayTestCase))
    return suite
