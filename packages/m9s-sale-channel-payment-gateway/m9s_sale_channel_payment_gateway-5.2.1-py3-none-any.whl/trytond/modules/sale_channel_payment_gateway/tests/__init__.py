# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

try:
    from trytond.modules.sale_channel_payment_gateway.tests.test_sale_channel_payment_gateway import suite
except ImportError:
    from .test_sale_channel_payment_gateway import suite

__all__ = ['suite']
