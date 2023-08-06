# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.transaction import Transaction
from trytond.pool import PoolMeta, Pool


class Sale(metaclass=PoolMeta):
    __name__ = 'sale.sale'

    @classmethod
    def __setup__(cls):
        super(Sale, cls).__setup__()
        cls.payment_authorize_on.states = cls.channel.states
        cls.payment_capture_on.states = cls.channel.states

    @classmethod
    def default_payment_authorize_on(cls):
        pool = Pool()
        Channel = pool.get('sale.channel')
        if Transaction().context.get('current_channel'):
            channel = Channel(Transaction().context['current_channel'])
            if channel.payment_authorize_on:
                return channel.payment_authorize_on
        return super(Sale, cls).default_payment_authorize_on()

    @classmethod
    def default_payment_capture_on(cls):
        pool = Pool()
        Channel = pool.get('sale.channel')
        if Transaction().context.get('current_channel'):
            channel = Channel(Transaction().context['current_channel'])
            if channel.payment_capture_on:
                return channel.payment_capture_on
        return super(Sale, cls).default_payment_capture_on()

    def on_change_channel(self):
        pool = Pool()
        SaleConfiguration = pool.get('sale.configuration')
        super(Sale, self).on_change_channel()
        if not self.channel:
            return
        if self.channel.payment_authorize_on:
            self.payment_authorize_on = self.channel.payment_authorize_on
        else:
            self.payment_authorize_on = \
                SaleConfiguration(1).payment_authorize_on
        if self.channel.payment_capture_on:
            self.payment_capture_on = self.channel.payment_capture_on
        else:
            self.payment_capture_on = SaleConfiguration(1).payment_capture_on

    def process_to_channel_state(self, channel_state):
        """
        Process the sale in tryton based on the state of order
        when its imported from channel.

        :param channel_state: State on external channel the order was imported.
        """
        pool = Pool()
        Sale = pool.get('sale.sale')
        Payment = pool.get('sale.payment')

        super(Sale, self).process_to_channel_state(channel_state)

        data = self.channel.get_tryton_action(channel_state)

        if data['action'] == 'import_as_past' and self.state == 'draft':
            Payment.delete(self.payments)
            # XXX: mark past orders as completed
            self.state = 'done'
            self.save()
            # Update cached values
            Sale.store_cache([self])


class SaleLine(metaclass=PoolMeta):
    "Sale Line"
    __name__ = 'sale.line'

    def create_payment_from(self, payment_data):
        """
        Create sale payment using given data.

        Since external channels are implemented by downstream modules, it is
        the responsibility of those channels to reuse this method.

        :param payment_data: Dictionary which must have at least one key-value
                                pair for 'code'
        """
        raise NotImplementedError(
            "This feature has not been implemented for %s channel yet."
            % self.source)
