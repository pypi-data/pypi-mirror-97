# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import PoolMeta, Pool
from trytond.model import ModelView, fields, ModelSQL, Unique
from trytond.pyson import Eval
from trytond.model import fields

STATES = {
    'readonly': ~Eval('active', True),
    }
DEPENDS = ['active']


class SaleChannel(metaclass=PoolMeta):
    __name__ = 'sale.channel'

    payment_authorize_on = fields.Selection(
        'get_authorize_options', 'Payment Authorize', states=STATES,
        depends=DEPENDS,
        help='Configure the payment authorize method for this channel. '
        'If empty, the default from Sale configuration is used.'
    )
    payment_capture_on = fields.Selection(
        'get_capture_options', 'Payment Capture', states=STATES,
        depends=DEPENDS,
        help='Configure the payment capture method for this channel. '
        'If empty, the default from Sale configuration is used.'
    )
    payment_gateways = fields.One2Many(
        'sale.channel.payment_gateway', 'channel', 'Payment Gateways'
    )

    @classmethod
    def get_authorize_options(cls):
        SaleConfiguration = Pool().get('sale.configuration')
        field_name = 'payment_authorize_on'
        selection = SaleConfiguration.fields_get(
            [field_name])[field_name]['selection']
        selection.insert(0, ('', ''))
        return selection

    @classmethod
    def get_capture_options(cls):
        SaleConfiguration = Pool().get('sale.configuration')
        field_name = 'payment_capture_on'
        selection = SaleConfiguration.fields_get(
            [field_name])[field_name]['selection']
        selection.insert(0, ('', ''))
        return selection


class ChannelPaymentGateway(ModelSQL, ModelView):
    """
    Sale Channel Payment Gateway
    """
    __name__ = 'sale.channel.payment_gateway'

    code = fields.Char("Code", required=True, select=True)
    name = fields.Char('Name', required=True)
    gateway = fields.Many2One(
        'payment_gateway.gateway', 'Gateway', required=True,
        ondelete='RESTRICT', select=True,
    )
    channel = fields.Many2One(
        'sale.channel', 'Channel', readonly=True, select=True,
    )

    @classmethod
    def __setup__(cls):
        """
        Setup the class before adding to pool
        """
        super(ChannelPaymentGateway, cls).__setup__()
        table = cls.__table__()
        cls._sql_constraints += [
            (
                'code_channel_unique',
                Unique(table, table.code, table.channel),
                'Payment gateway already exists for this channel'
            )
        ]

    @classmethod
    def find_gateway_using_channel_data(cls, channel, gateway_data):
        """
        Search for an existing gateway by matching code and channel.
        If found, return its active record else None
        """
        try:
            gateway, = cls.search([
                ('code', '=', gateway_data['code']),
                ('channel', '=', channel.id),
            ])
        except ValueError:
            return None
        else:
            return gateway


