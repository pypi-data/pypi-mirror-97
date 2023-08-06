# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
import unittest

from decimal import Decimal

from trytond.tests.test_tryton import ModuleTestCase, with_transaction
from trytond.tests.test_tryton import suite as test_suite
from trytond.transaction import Transaction
from trytond.pool import Pool
from trytond.exceptions import UserError
from trytond.model.modelstorage import DomainValidationError

from trytond.modules.company.tests import set_company
from trytond.modules.payment_gateway.tests import create_payment_gateway
from trytond.modules.invoice_payment_gateway.tests import create_payment_term
from trytond.modules.sale_payment_gateway.tests import create_sale


def setup_users():
    pool = Pool()
    Company = pool.get('company.company')
    User = pool.get('res.user')
    Model = Pool().get('ir.model.data')

    # Setup users
    sales_users = User.search([
                ('login', '=', 'sale'),
                ])
    if not sales_users:
        company, = Company.search([])
        group_sale_admin_id = Model.get_id('sale', 'group_sale_admin')
        group_sale_id = Model.get_id('sale', 'group_sale')

        with set_company(company):
            basic_user, = User.create([{
                        'name': 'Basic User',
                        'login': 'basic',
                        'company': company,
                        'main_company': company,
                        }])
            sales_user, = User.create([{
                        'name': 'Sales Person',
                        'login': 'sale',
                        'company': company,
                        'main_company': company,
                        'groups': [('add', [
                                    group_sale_id,
                                    ])]
                        }])
            sales_admin, = User.create([{
                        'name': 'Sales Admin',
                        'login': 'sale_admin',
                        'company': company,
                        'main_company': company,
                        'groups': [('add', [
                                    group_sale_admin_id,
                                ])]
                        }])
    else:
        sales_user = sales_users[0]
        basic_user, = User.search([
                    ('login', '=', 'basic'),
                    ])
        sales_admin, = User.search([
                    ('login', '=', 'sale_admin'),
                    ])
    users = {
        'basic_user': basic_user,
        'sales_user': sales_user,
        'sales_admin': sales_admin,
        }
    return users


def create_channel_sale(user=None, channel=None):
    pool = Pool()
    Company = pool.get('company.company')
    SaleChannel = pool.get('sale.channel')

    # Create the channels
    company, = Company.search([])
    users = setup_users()
    if not SaleChannel.search([]):
        create_sale_channels(company)

    if not user:
        users = setup_users()
        user = users['basic_user']
    with Transaction().set_user(user.id) as u, Transaction().set_context(
            company=company.id,
            current_channel=channel,
            language='en') as c:
                channel_sale = create_sale()
                channel_sale.save()
                channel_sale.on_change_channel()
    return channel_sale


def create_sale_channels(company):
    pool = Pool()
    Location = pool.get('stock.location')
    PriceList = pool.get('product.price_list')
    SaleChannel = pool.get('sale.channel')

    with Transaction().set_context(company=company.id):
        price_list = PriceList(
            name='PL 1',
            company=company
            )
        price_list.save()

        address = company.party.addresses[0]
        warehouse, = Location.search([
                ('code', '=', 'WH')
                ])
        users = setup_users()
        basic_user = users['basic_user']
        sales_user = users['sales_user']
        payment_term = create_payment_term()

        channel1, channel2, channel3, channel4 = \
            SaleChannel.create([{
                'name': 'Channel 1',
                'code': 'C1',
                'address': address,
                'source': 'manual',
                'timezone': 'UTC',
                'warehouse': warehouse,
                'invoice_method': 'manual',
                'shipment_method': 'manual',
                'payment_term': payment_term.id,
                'price_list': price_list,
            }, {
                'name': 'Channel 2',
                'code': 'C2',
                'address': address,
                'source': 'manual',
                'timezone': 'US/Pacific',
                'warehouse': warehouse,
                'invoice_method': 'manual',
                'shipment_method': 'manual',
                'payment_term': payment_term.id,
                'price_list': price_list,
                'read_users': [('add', [sales_user.id])],
            }, {
                'name': 'Channel 3',
                'code': 'C3',
                'address': address,
                'source': 'manual',
                'warehouse': warehouse,
                'invoice_method': 'manual',
                'shipment_method': 'manual',
                'payment_term': payment_term.id,
                'price_list': price_list,
                'read_users': [('add', [sales_user.id])],
                'create_users': [('add', [sales_user.id])],
            }, {
                'name': 'Channel 4',
                'code': 'C4',
                'address': address,
                'source': 'manual',
                'timezone': 'US/Eastern',
                'warehouse': warehouse,
                'invoice_method': 'manual',
                'shipment_method': 'manual',
                'payment_term': payment_term.id,
                'price_list': price_list,
                'read_users': [('add', [basic_user.id, sales_user.id])],
                'create_users': [('add', [basic_user.id])],
            }])


def create_product(name, vlist, uri, uom='Unit'):
    """
    Create a product template with products and return its ID
    :param name: Name of the product
    :param vlist: List of dictionaries of values to create
    :param uri: uri of product template
    :param uom: Note it is the name of UOM (not symbol or code)
    """
    pool = Pool()
    ProductTemplate = pool.get('product.template')
    Uom = pool.get('product.uom')

    uom, = Uom.search([('name', '=', uom)], limit=1)
    for values in vlist:
        values['name'] = name
        values['default_uom'] = uom
        values['sale_uom'] = uom
        values['products'] = [('create', [{}])]
    product, = ProductTemplate.create(vlist)
    return product


class SaleChannelPaymentGatewayTestCase(ModuleTestCase):
    'Test Sale Channel Payment Gateway module'
    module = 'sale_channel_payment_gateway'

    @with_transaction()
    def test_0005_channel_status_bar(self):
        pool = Pool()
        Company = pool.get('company.company')
        SaleChannel = pool.get('sale.channel')

        # Setup defaults
        # A gateway sets up a lot of configuration stuff (fiscalyear, chart,
        # etc.)
        gateway = create_payment_gateway()
        gateway.save()
        users = setup_users()
        sales_user = users['sales_user']
        company, = Company.search([])
        create_sale_channels(company)

        channel1, channel2, channel3, channel4 = SaleChannel.search(
            [], order=[('code', 'ASC')])

        sales_user.current_channel = channel3
        sales_user.save()

        self.assertTrue(channel3.rec_name in sales_user.status_bar)

    @with_transaction()
    def test_0010_channel_required(self):
        #      USER       Channel1    Channel2    Channel3  Channel4
        #    sale_admin      RW          RW          RW       RW
        #    sale_user       -           R           RW       R
        #    basic_user      -           -           -        RW
        pool = Pool()
        Company = pool.get('company.company')
        SaleChannel = pool.get('sale.channel')

        # Setup defaults
        # A gateway sets up a lot of configuration stuff (fiscalyear, chart,
        # etc.)
        gateway = create_payment_gateway()
        gateway.save()
        users = setup_users()
        sales_admin = users['sales_admin']
        company, = Company.search([])
        create_sale_channels(company)

        channel1, channel2, channel3, channel4 = SaleChannel.search(
            [], order=[('code', 'ASC')])

        # Test the custom UserError:
        # First go to user preferences and select a current_channel for "%s".
        with self.assertRaises(UserError):
            sale = create_channel_sale(sales_admin, channel1.id)

    @with_transaction()
    def test_0020_sales_admin(self):
        #      USER       Channel1    Channel2    Channel3  Channel4
        #    sale_admin      RW          RW          RW       RW
        #    sale_user       -           R           RW       R
        #    basic_user      -           -           -        RW
        pool = Pool()
        Company = pool.get('company.company')
        SaleChannel = pool.get('sale.channel')

        # Setup defaults
        # A gateway sets up a lot of configuration stuff (fiscalyear, chart,
        # etc.)
        gateway = create_payment_gateway()
        gateway.save()
        users = setup_users()
        sales_admin = users['sales_admin']
        company, = Company.search([])
        create_sale_channels(company)

        channel1, channel2, channel3, channel4 = SaleChannel.search(
            [], order=[('code', 'ASC')])

        with Transaction().set_user(sales_admin.id):
            sales_admin.current_channel = channel1
            sales_admin.save()
            sale = create_channel_sale(sales_admin, channel1.id)
            sales_admin.current_channel = channel2
            sales_admin.save()
            sale = create_channel_sale(sales_admin, channel2.id)
            sales_admin.current_channel = channel3
            sales_admin.save()
            sale = create_channel_sale(sales_admin, channel3.id)
            sales_admin.current_channel = channel3
            sales_admin.save()
            sale = create_channel_sale(sales_admin, channel4.id)

    @with_transaction()
    def test_0030_channel_permissions(self):
        #      USER       Channel1    Channel2    Channel3  Channel4
        #    sale_admin      RW          RW          RW       RW
        #    sale_user       -           R           RW       R
        #    basic_user      -           -           -        RW
        pool = Pool()
        Company = pool.get('company.company')
        User = pool.get('res.user')
        Sale = pool.get('sale.sale')
        SaleChannel = pool.get('sale.channel')
        transaction = Transaction()

        # Setup defaults
        # A gateway sets up a lot of configuration stuff (fiscalyear, chart,
        # etc.)
        def setup_defaults():
            gateway = create_payment_gateway()
            gateway.save()
            users = setup_users()
            basic_user = users['basic_user']
            sales_user = users['sales_user']
            company, = Company.search([])
            create_sale_channels(company)

            channel1, channel2, channel3, channel4 = SaleChannel.search(
                [], order=[('code', 'ASC')])
            return (basic_user, sales_user, company, channel1, channel2,
                channel3, channel4)

        basic_user, sales_user, company, channel1, \
            channel2, channel3, channel4 = setup_defaults()
        # Raise user error with missing channel
        with self.assertRaises(UserError):
            sale = create_channel_sale()
        transaction.rollback()

        basic_user, sales_user, company, channel1, \
            channel2, channel3, channel4 = setup_defaults()
        # Raise the domain validation error with not allowed channel for the
        # user:
        # The value for field "Current Channel" in "User" is not valid
        # according to its domain
        with Transaction().set_user(sales_user.id):
            sales_user.current_channel = channel1
            sales_user.save()
            with self.assertRaises(DomainValidationError):
                sale = create_channel_sale(user=sales_user,
                    channel=channel1.id)
        transaction.rollback()

        basic_user, sales_user, company, channel1, \
            channel2, channel3, channel4 = setup_defaults()
        # With only read permissions
        # UserError: You cannot work on orders of this channel
        # because you do not have the required permissions.
        sales_user.current_channel = channel2
        sales_user.save()
        with self.assertRaises(UserError):
            sale = create_channel_sale(user=sales_user,
                channel=channel2.id)
        transaction.rollback()

        basic_user, sales_user, company, channel1, \
            channel2, channel3, channel4 = setup_defaults()
        # Success with create permissions
        sales_user.current_channel = channel3
        sales_user.save()
        sale1 = create_channel_sale(user=sales_user,
            channel=channel3.id)
        self.assertEqual(sale1.invoice_method, 'manual')
        self.assertEqual(sale1.channel_type, channel3.source)

        # Try to edit a sale with only read permissions
        # Create the sale in channel4 with basic_user
        basic_user.current_channel = channel4
        basic_user.save()
        sale2 = create_channel_sale(user=basic_user,
            channel=channel4.id)
        sale_description = 'Description by %s' % basic_user.name
        sale2.description = sale_description
        sale2.save()

        # The sales_user has read, but not write permissions
        # Try to edit the former sale with the sales_user
        sales_user.current_channel = channel4
        sales_user.save()
        with Transaction().set_user(sales_user.id):
            sale2 = Sale(sale2.id)
            self.assertEqual(sale2.reference, 'Test Sale')
            self.assertEqual(sale2.description, sale_description)
            # UserError: You cannot work on orders of this channel
            # because you do not have the required permissions.
            with self.assertRaises(UserError):
                sale2.description = 'changed'
                sale2.save()
        transaction.rollback()

    @with_transaction()
    def test_0050_check_duplicate_channel_identifier_for_sale(self):
        """
        Check if error is raised for duplicate channel identifier in sale
        """
        pool = Pool()
        Company = pool.get('company.company')
        SaleChannel = pool.get('sale.channel')

        # Setup defaults
        # A gateway sets up a lot of configuration stuff (fiscalyear, chart,
        # etc.)
        gateway = create_payment_gateway()
        gateway.save()
        users = setup_users()
        sales_user = users['sales_user']
        company, = Company.search([])
        create_sale_channels(company)

        channel1, channel2, channel3, channel4 = SaleChannel.search(
            [], order=[('code', 'ASC')])

        sales_user.current_channel = channel3
        sales_user.save()
        sale1 = create_channel_sale(user=sales_user,
            channel=channel3.id)
        sale2 = create_channel_sale(user=sales_user,
            channel=channel3.id)

        sale1.channel_identifier = 'Test Sale 1'
        sale1.save()

        # Same channel identifier for sale 2 should raise error
        with self.assertRaises(UserError):
            sale2.channel_identifier = 'Test Sale 1'
            sale2.save()

    @with_transaction()
    def test_0060_return_sale_with_channel_identifier(self):
        """
        Check if return sale works with channel_identifier
        """
        pool = Pool()
        Company = pool.get('company.company')
        Sale = pool.get('sale.sale')
        SaleChannel = pool.get('sale.channel')
        ReturnSale = pool.get('sale.return_sale', type='wizard')

        # Setup defaults
        # A gateway sets up a lot of configuration stuff (fiscalyear, chart,
        # etc.)
        gateway = create_payment_gateway()
        gateway.save()
        users = setup_users()
        sales_user = users['sales_user']
        company, = Company.search([])
        create_sale_channels(company)

        channel1, channel2, channel3, channel4 = SaleChannel.search(
            [], order=[('code', 'ASC')])

        sales_user.current_channel = channel3
        sales_user.save()
        sale1 = create_channel_sale(user=sales_user,
            channel=channel3.id)
        sale2 = create_channel_sale(user=sales_user,
            channel=channel3.id)

        sale1.channel_identifier = 'Test Sale 1'
        sale1.save()

        # Return sale with channel identifier
        session_id, _, _ = ReturnSale.create()
        return_sale = ReturnSale(session_id)

        with Transaction().set_user(sales_user.id):
            with Transaction().set_context(active_ids=[sale1.id]):
                return_sale.do_return_(return_sale.return_.get_action())

            # Return a sale with lines
            sale2.channel_identifier = 'Test Sale 2'
            sale2.save()
            Sale.write([sale2], {
                'lines': [
                    ('create', [{
                        'type': 'comment',
                        'channel_identifier': 'Test Sale Line',
                        'description': 'Test Desc'
                    }])
                ]
            })

            session_id, _, _ = ReturnSale.create()
            return_sale = ReturnSale(session_id)
            with Transaction().set_context(active_ids=[sale2.id]):
                return_sale.do_return_(return_sale.return_.get_action())

    @with_transaction()
    def test_0080_map_tax(self):
        """
        Check if tax is mapped
        """
        pool = Pool()
        Company = pool.get('company.company')
        SaleChannel = pool.get('sale.channel')
        SaleChannelTax = pool.get('sale.channel.tax')
        Tax = pool.get('account.tax')
        Account = pool.get('account.account')

        # Setup defaults
        # A gateway sets up a lot of configuration stuff (fiscalyear, chart,
        # etc.)
        gateway = create_payment_gateway()
        gateway.save()
        company, = Company.search([])
        create_sale_channels(company)

        channel1, channel2, channel3, channel4 = SaleChannel.search(
            [], order=[('code', 'ASC')])

        with set_company(company):
            cash, = Account.search([
                    ('type.receivable', '=', True),
                    ('type.statement', '=', 'balance'),
                    ])
            tax1, = Tax.create([
                {
                    'name': "tax1",
                    'description': "Tax description",
                    'type': 'percentage',
                    'company': company.id,
                    'invoice_account': cash,
                    'credit_note_account': cash,
                    'rate': Decimal('8.00'),
                }
            ])

        mapped_tax, = SaleChannelTax.create([{
            'name': 'new_channel_tax',
            'rate': Decimal('8.00'),
            'tax': tax1.id,
            'channel': channel1.id,
            }])

        self.assertEqual(
            channel1.get_tax('new_channel_tax', Decimal('8.00')), tax1)

    @with_transaction()
    def test_0100_check_channel_exception(self):
        """
        Check if channel exception is being created
        """
        pool = Pool()
        Company = pool.get('company.company')
        SaleChannel = pool.get('sale.channel')
        ChannelException = pool.get('channel.exception')

        # Setup defaults
        # A gateway sets up a lot of configuration stuff (fiscalyear, chart,
        # etc.)
        gateway = create_payment_gateway()
        gateway.save()
        users = setup_users()
        sales_user = users['sales_user']
        company, = Company.search([])
        create_sale_channels(company)

        channel1, channel2, channel3, channel4 = SaleChannel.search(
            [], order=[('code', 'ASC')])

        sales_user.current_channel = channel3
        sales_user.save()
        sale = create_channel_sale(user=sales_user,
            channel=channel3.id)
        self.assertEqual(sale.invoice_method, 'manual')
        self.assertEqual(sale.channel_type, channel3.source)

        self.assertFalse(sale.has_channel_exception)

        channel_exception, = ChannelException.create([{
            'origin': '%s,%s' % (sale.__name__, sale.id),
            'log': 'Sale has exception',
            'channel': sale.channel.id,
            }])

        self.assertTrue(channel_exception)
        self.assertTrue(sale.has_channel_exception)

        # Mark exception as resolved
        channel_exception.is_resolved = True
        channel_exception.save()

        self.assertFalse(sale.has_channel_exception)

    @with_transaction()
    def test_0110_check_channel_exception_searcher(self):
        """
        Check searcher for channel exception
        """
        pool = Pool()
        Company = pool.get('company.company')
        Sale = pool.get('sale.sale')
        SaleChannel = pool.get('sale.channel')
        ChannelException = pool.get('channel.exception')

        # Setup defaults
        # A gateway sets up a lot of configuration stuff (fiscalyear, chart,
        # etc.)
        gateway = create_payment_gateway()
        gateway.save()
        users = setup_users()
        sales_user = users['sales_user']
        company, = Company.search([])
        create_sale_channels(company)

        channel1, channel2, channel3, channel4 = SaleChannel.search(
            [], order=[('code', 'ASC')])

        sales_user.current_channel = channel3
        sales_user.save()
        sale1 = create_channel_sale(user=sales_user,
            channel=channel3.id)
        sale2 = create_channel_sale(user=sales_user,
            channel=channel3.id)
        sale3 = create_channel_sale(user=sales_user,
            channel=channel3.id)

        self.assertFalse(sale1.has_channel_exception)
        self.assertFalse(sale2.has_channel_exception)

        self.assertEqual(Sale.search([
                    ('has_channel_exception', '=', True),
                    ], count=True), 0)
        self.assertEqual(Sale.search([
                    ('has_channel_exception', '=', False),
                    ], count=True), 3)

        ChannelException.create([{
                    'origin': '%s,%s' % (sale1.__name__, sale1.id),
                    'log': 'Sale has exception',
                    'channel': sale1.channel.id,
                    'is_resolved': False,
                    }])

        ChannelException.create([{
                    'origin': '%s,%s' % (sale2.__name__, sale2.id),
                    'log': 'Sale has exception',
                    'channel': sale2.channel.id,
                    'is_resolved': True,
                    }])

        self.assertEqual(Sale.search([('has_channel_exception', '=', True)]),
            [sale1])

        # Sale2 has exception but is resolved already
        self.assertEqual(Sale.search([('has_channel_exception', '=', False)]),
            [sale3, sale2])

    @with_transaction()
    def test_0200_orders_import_wizard(self):
        """
        Check orders import wizard
        """
        pool = Pool()
        Company = pool.get('company.company')
        SaleChannel = pool.get('sale.channel')
        Account = pool.get('account.account')
        AccountConfiguration = pool.get('account.configuration')
        ImportDataWizard = pool.get('sale.channel.import_data', type='wizard')

        # Setup defaults
        # A gateway sets up a lot of configuration stuff (fiscalyear, chart,
        # etc.)
        gateway = create_payment_gateway()
        gateway.save()
        company, = Company.search([])
        create_sale_channels(company)

        channel1, channel2, channel3, channel4 = SaleChannel.search(
            [], order=[('code', 'ASC')])

        with Transaction().set_context(active_id=channel1, company=company.id):
            session_id, start_state, end_state = ImportDataWizard.create()
            ImportDataWizard.execute(session_id, {}, start_state)
            import_data = ImportDataWizard(session_id)
            import_data.start.import_orders = True
            import_data.start.import_products = True
            import_data.start.channel = channel1

            # Product / Order is being imported but default accounts are not
            # set. So it will ask for accounts first
            self.assertFalse(import_data.get_default_account('revenue'))
            self.assertFalse(import_data.get_default_account('expense'))

            self.assertEqual(import_data.transition_next(), 'choose_accounts')

            with set_company(company):
                revenue, = Account.search([
                        ('type.revenue', '=', True),
                        ])
                expense, = Account.search([
                        ('type.expense', '=', True),
                        ])

            # Configure default accounts
            configuration = AccountConfiguration(1)
            configuration.default_category_account_expense = expense
            configuration.default_category_account_revenue = revenue
            configuration.save()
            self.assertTrue(import_data.get_default_account('revenue'))
            self.assertTrue(import_data.get_default_account('expense'))

            # Since default accounts are set, it wont ask for choose_accounts
            # again
            self.assertEqual(import_data.transition_next(), 'import_')

            with self.assertRaises(NotImplementedError):
                # NotImplementedError is thrown in this case.
                # Importing orders feature is not available in this module
                import_data.transition_import_()

    @with_transaction()
    def test_0210_channel_availability(self):
        pool = Pool()
        StockMove = pool.get('stock.move')
        Location = pool.get('stock.location')
        SaleChannel = pool.get('sale.channel')
        Company = pool.get('company.company')

        # Setup defaults
        # A gateway sets up a lot of configuration stuff (fiscalyear, chart,
        # etc.)
        gateway = create_payment_gateway()
        gateway.save()
        company, = Company.search([])
        create_sale_channels(company)

        channel1, channel2, channel3, channel4 = SaleChannel.search(
            [], order=[('code', 'ASC')])

        # Create product templates with products
        template1 = create_product(
            'product-1',
            [{
                'type': 'goods',
                'salable': True,
                'list_price': Decimal('10'),
            }],
            uri='product-1',
        )
        template2 = create_product(
            'product-2',
            [{
                'type': 'goods',
                'salable': True,
                'list_price': Decimal('15'),
            }],
            uri='product-2',
        )

        product1 = template1.products[0]
        product2 = template2.products[0]

        self.assertEqual(
            channel1.get_availability(product1),
            {'type': 'bucket', 'value': 'out_of_stock'}
            )
        self.assertEqual(
            channel1.get_availability(product2),
            {'type': 'bucket', 'value': 'out_of_stock'}
            )

        lost_and_found, = Location.search([
            ('type', '=', 'lost_found')
            ])
        with Transaction().set_context(company=company.id):
            # Make inventory for product 1
            move, = StockMove.create([{
                'from_location': lost_and_found,
                'to_location': channel1.warehouse.storage_location,
                'quantity': 10,
                'product': product1,
                'uom': product1.default_uom,
                }])
            StockMove.do([move])

        self.assertEqual(
            channel1.get_availability(product1),
            {'type': 'bucket', 'value': 'in_stock'}
            )
        self.assertEqual(
            channel1.get_availability(product2),
            {'type': 'bucket', 'value': 'out_of_stock'}
            )


def suite():
    suite = test_suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
            SaleChannelPaymentGatewayTestCase))
    return suite

