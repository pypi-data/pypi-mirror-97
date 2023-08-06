# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
import unittest

from decimal import Decimal
from dateutil.relativedelta import relativedelta

from trytond.tests.test_tryton import ModuleTestCase, with_transaction
from trytond.tests.test_tryton import suite as test_suite
from trytond.transaction import Transaction
from trytond.pool import Pool
from trytond.exceptions import UserError

from trytond.modules.account.tests import create_chart, get_fiscalyear
from trytond.modules.company.tests import create_company, set_company
from trytond.modules.account_invoice.tests import set_invoice_sequences
from trytond.modules.payment_gateway.tests import (create_payment_transaction,
    create_payment_profile)


def create_write_off():
    """
    Create a Reconcile Write Off and write it to the account configuration
    """
    pool = Pool()
    Company = pool.get('company.company')
    WriteOff = pool.get('account.move.reconcile.write_off')
    AccountConfiguration = pool.get('account.configuration')
    Journal = pool.get('account.journal')
    Account = pool.get('account.account')
    Sequence = pool.get('ir.sequence')

    company, = Company.search([])
    with set_company(company):
        revenue, = Account.search([
                ('type.revenue', '=', True),
                ])
        expense, = Account.search([
                ('type.expense', '=', True),
                ])

    sequence_journal, = Sequence.search([
            ('code', '=', 'account.journal'),
            ])
    journal_write_off = Journal()
    journal_write_off.name = 'Write Off Journal'
    journal_write_off.type = 'write-off'
    journal_write_off.sequence = sequence_journal
    journal_write_off.save()

    write_off = WriteOff()
    write_off.name = 'Write Off'
    write_off.company = company
    write_off.credit_account = revenue
    write_off.debit_account = expense
    write_off.journal = journal_write_off
    write_off.save()

    account_config = AccountConfiguration(1)
    account_config.write_off = write_off
    account_config.save()


def create_payment_term():
    """Create a simple payment term with all advance
    """
    pool = Pool()
    PaymentTerm = pool.get('account.invoice.payment_term')

    return PaymentTerm.create([{
        'name': 'Direct',
        'lines': [('create', [{'type': 'remainder'}])]
        }])[0]


def create_products():
    pool = Pool()
    Account = pool.get('account.account')
    Company = pool.get('company.company')
    ProductCategory = pool.get('product.category')
    Template = pool.get('product.template')
    Product = pool.get('product.product')
    Uom = pool.get('product.uom')

    company, = Company.search([])
    with set_company(company):
        revenue, = Account.search([
                ('type.revenue', '=', True),
                ])
        expense, = Account.search([
                ('type.expense', '=', True),
                ])

        with Transaction().set_context(company=company.id):
            product_category, = ProductCategory.create([{
                        'name': 'Test Category',
                        'account_revenue': revenue,
                        'account_expense': expense,
                        'accounting': True,
                        }])

            uom, = Uom.search([('symbol', '=', 'd')])
            product_template, = Template.create([{
                'name': 'Toy',
                'type': 'goods',
                'list_price': Decimal('10'),
                'categories': [('add', [product_category.id])],
                'account_category': product_category.id,
                'default_uom': uom,
                }])

            product1, = Product.create([{
                'template': product_template.id,
                'code': 'toy-1',
                'cost_price': Decimal('5'),
                }])
            product2, = Product.create([{
                'template': product_template.id,
                'code': 'toy-2',
                'cost_price': Decimal('5'),
                }])


def create_and_post_invoice(party):
    """
    Create and post an invoice for the party
    """
    pool = Pool()
    Company = pool.get('company.company')
    Journal = pool.get('account.journal')
    Account = pool.get('account.account')
    Invoice = pool.get('account.invoice')
    Date = pool.get('ir.date')
    Product = pool.get('product.product')

    company, = Company.search([])
    with set_company(company):
        journal_revenue, = Journal.search([
                ('code', '=', 'REV'),
                ])
        journal_expense, = Journal.search([
                ('code', '=', 'EXP'),
                ])
        journal_cash, = Journal.search([
                ('code', '=', 'CASH'),
                ])
        revenue, = Account.search([
                ('type.revenue', '=', True),
                ])
        receivable, = Account.search([
                ('type.receivable', '=', True),
                ])
        expense, = Account.search([
                ('type.expense', '=', True),
                ])
        payable, = Account.search([
                ('type.payable', '=', True),
                ])
        cash, = Account.search([
                ('name', '=', 'Main Cash'),
                ])

    party.account_receivable = receivable
    party.save()

    with Transaction().set_context(company=company.id):
        payment_term = create_payment_term()
        create_products()
        product1, = Product.search([('code', '=', 'toy-1')])
        product2, = Product.search([('code', '=', 'toy-2')])
        invoice, = Invoice.create([{
            'party': party,
            'type': 'out',
            'journal': journal_revenue,
            'invoice_address': party.address_get('invoice'),
            'account': receivable,
            'description': 'Test Invoice',
            'payment_term': payment_term,
            'invoice_date': Date.today(),
            'lines': [('create', [{
                'product': product1.id,
                'description': product1.rec_name,
                'quantity': 10,
                'unit_price': Decimal('10.00'),
                'unit': product1.default_uom,
                'account': product1.account_revenue_used
                }, {
                'product': product2.id,
                'description': product2.rec_name,
                'quantity': 10,
                'unit_price': Decimal('20.00'),
                'unit': product2.default_uom,
                'account': product2.account_revenue_used
                }])]
            }])

    Invoice.post([invoice])
    return invoice


class InvoicePaymentGatewayTestCase(ModuleTestCase):
    'Test Invoice Payment Gateway module'
    module = 'invoice_payment_gateway'

    @with_transaction()
    def test_0010_test_paying_invoice_with_cash(self):
        """
        Create and pay an invoice using payment transaction
        """
        pool = Pool()
        Company = pool.get('company.company')
        Wizard = pool.get('account.invoice.pay_using_transaction',
            type='wizard')

        transaction = create_payment_transaction()
        invoice = create_and_post_invoice(transaction.party)
        self.assertTrue(invoice)
        self.assertEqual(invoice.state, 'posted')
        self.assertTrue(invoice.amount_to_pay)

        company, = Company.search([])
        # Pay invoice using cash transaction
        with Transaction().set_context(active_id=invoice.id):
            pay_wizard = Wizard(Wizard.create()[0])
            defaults = pay_wizard.default_start()

            pay_wizard.start.invoice = defaults['invoice']
            pay_wizard.start.party = defaults['party']
            pay_wizard.start.company = defaults['company']
            pay_wizard.start.credit_account = defaults['credit_account']
            pay_wizard.start.owner = defaults['owner']
            pay_wizard.start.currency_digits = defaults['currency_digits']
            pay_wizard.start.amount = defaults['amount']
            pay_wizard.start.user = defaults['user']
            pay_wizard.start.gateway = transaction.gateway.id
            pay_wizard.start.payment_profile = None
            pay_wizard.start.reference = 'Test paying with cash'
            pay_wizard.start.method = transaction.gateway.method
            pay_wizard.start.transaction_type = defaults['transaction_type']

            with Transaction().set_context(company=company.id):
                pay_wizard.transition_pay()

        self.assertEqual(invoice.state, 'paid')
        self.assertFalse(invoice.amount_to_pay)

    @with_transaction()
    def test_0020_test_paying_invoice_with_new_credit_card(self):
        """
        Create and pay an invoice using payment transaction
        """
        pool = Pool()
        Company = pool.get('company.company')
        Date = pool.get('ir.date')
        Wizard = pool.get(
            'account.invoice.pay_using_transaction', type='wizard')

        transaction = create_payment_transaction(method='dummy')
        invoice = create_and_post_invoice(transaction.party)
        self.assertTrue(invoice)
        self.assertEqual(invoice.state, 'posted')
        self.assertTrue(invoice.amount_to_pay)

        company, = Company.search([])
        # Pay invoice using card transaction
        with Transaction().set_context(active_id=invoice.id):
            pay_wizard = Wizard(Wizard.create()[0])
            defaults = pay_wizard.default_start()

            pay_wizard.start.invoice = defaults['invoice']
            pay_wizard.start.party = defaults['party']
            pay_wizard.start.company = defaults['company']
            pay_wizard.start.credit_account = defaults['credit_account']
            pay_wizard.start.owner = defaults['owner']
            pay_wizard.start.currency_digits = defaults['currency_digits']
            pay_wizard.start.amount = defaults['amount']
            pay_wizard.start.user = defaults['user']
            pay_wizard.start.gateway = transaction.gateway.id
            pay_wizard.start.payment_profile = None
            pay_wizard.start.reference = 'Test paying with new card'
            pay_wizard.start.method = transaction.gateway.method
            pay_wizard.start.use_existing_card = False
            pay_wizard.start.number = '4111111111111111'
            pay_wizard.start.expiry_month = '05'
            pay_wizard.start.expiry_year = '%s' % (Date.today().year + 3)
            pay_wizard.start.csc = '435'
            pay_wizard.start.provider = transaction.gateway.provider
            pay_wizard.start.transaction_type = defaults['transaction_type']

            with Transaction().set_context(company=company.id):
                pay_wizard.transition_pay()

        self.assertEqual(invoice.state, 'paid')
        self.assertFalse(invoice.amount_to_pay)

    @with_transaction()
    def test_0030_test_paying_invoice_with_saved_credit_card(self):
        """
        Create and pay an invoice using a payment profile
        """
        pool = Pool()
        Company = pool.get('company.company')
        Wizard = pool.get(
            'account.invoice.pay_using_transaction', type='wizard')

        transaction = create_payment_transaction(method='dummy')
        invoice = create_and_post_invoice(transaction.party)
        self.assertTrue(invoice)
        self.assertEqual(invoice.state, 'posted')
        self.assertTrue(invoice.amount_to_pay)

        profile = create_payment_profile(invoice.party, transaction.gateway)
        self.assertTrue(profile)

        company, = Company.search([])
        # Pay invoice using cash transaction
        with Transaction().set_context(active_id=invoice.id):
            pay_wizard = Wizard(Wizard.create()[0])
            defaults = pay_wizard.default_start()

            pay_wizard.start.invoice = defaults['invoice']
            pay_wizard.start.party = defaults['party']
            pay_wizard.start.company = defaults['company']
            pay_wizard.start.credit_account = defaults['credit_account']
            pay_wizard.start.owner = defaults['owner']
            pay_wizard.start.currency_digits = defaults['currency_digits']
            pay_wizard.start.amount = defaults['amount']
            pay_wizard.start.user = defaults['user']
            pay_wizard.start.gateway = transaction.gateway.id
            pay_wizard.start.payment_profile = profile
            pay_wizard.start.reference = 'Test paying with profile'
            pay_wizard.start.method = transaction.gateway.method
            pay_wizard.start.use_existing_card = True
            pay_wizard.start.transaction_type = defaults['transaction_type']

            with Transaction().set_context(company=company.id):
                pay_wizard.transition_pay()

        self.assertEqual(invoice.state, 'paid')
        self.assertFalse(invoice.amount_to_pay)

    @with_transaction()
    def test_0040_test_paying_invoice_write_off(self):
        """
        Test invoice pay logic with write-off
        """
        pool = Pool()
        Company = pool.get('company.company')
        AccountMove = pool.get('account.move')
        AccountConfiguration = pool.get('account.configuration')
        Wizard = pool.get(
            'account.invoice.pay_using_transaction', type='wizard')

        account_config = AccountConfiguration(1)
        self.assertEqual(account_config.write_off_threshold, Decimal('0'))

        transaction = create_payment_transaction()
        invoice = create_and_post_invoice(transaction.party)
        self.assertTrue(invoice)
        self.assertEqual(invoice.state, 'posted')
        self.assertTrue(invoice.amount_to_pay)

        company, = Company.search([])

        create_write_off()
        self.assertTrue(account_config.write_off)

        # Pay invoice using cash transaction
        with Transaction().set_context(active_id=invoice.id):
            pay_wizard = Wizard(Wizard.create()[0])
            defaults = pay_wizard.default_start()

            pay_wizard.start.invoice = defaults['invoice']
            pay_wizard.start.party = defaults['party']
            pay_wizard.start.company = defaults['company']
            pay_wizard.start.credit_account = defaults['credit_account']
            pay_wizard.start.owner = defaults['owner']
            pay_wizard.start.currency_digits = defaults['currency_digits']
            pay_wizard.start.amount = defaults['amount'] - Decimal('0.02')
            pay_wizard.start.user = defaults['user']
            pay_wizard.start.gateway = transaction.gateway.id
            pay_wizard.start.payment_profile = None
            pay_wizard.start.reference = 'Test paying with cash'
            pay_wizard.start.method = transaction.gateway.method
            pay_wizard.start.transaction_type = defaults['transaction_type']

            with Transaction().set_context(company=company.id):
                pay_wizard.transition_pay()

        self.assertEqual(invoice.state, 'posted')
        self.assertTrue(invoice.amount_to_pay)

        # Set the write-off threshold and pay invoice again.
        account_config.write_off_threshold = Decimal('0.01')
        account_config.save()

        with Transaction().set_context(active_id=invoice.id):
            pay_wizard = Wizard(Wizard.create()[0])
            defaults = pay_wizard.default_start()

            pay_wizard.start.invoice = defaults['invoice']
            pay_wizard.start.party = defaults['party']
            pay_wizard.start.company = defaults['company']
            pay_wizard.start.credit_account = defaults['credit_account']
            pay_wizard.start.owner = defaults['owner']
            pay_wizard.start.currency_digits = defaults['currency_digits']
            pay_wizard.start.amount = Decimal('0.01')
            pay_wizard.start.user = defaults['user']
            pay_wizard.start.gateway = transaction.gateway.id
            pay_wizard.start.payment_profile = None
            pay_wizard.start.reference = 'Test paying with cash'
            pay_wizard.start.method = transaction.gateway.method
            pay_wizard.start.transaction_type = defaults['transaction_type']

            with Transaction().set_context(company=company.id):
                pay_wizard.transition_pay()

        self.assertEqual(invoice.state, 'paid')
        self.assertFalse(invoice.amount_to_pay)

        # There should be one journal entry on writeoff
        self.assertEqual(AccountMove.search_count([
                    ('journal', '=', account_config.write_off.journal)
                    ]), 1)

    @with_transaction()
    def test_0050_test_paying_invoice_write_off_zero_amount_moves(self):
        """
        Paying an invoice should not create any (zero amount) write-off entry
        """
        pool = Pool()
        Company = pool.get('company.company')
        AccountMove = pool.get('account.move')
        AccountConfiguration = pool.get('account.configuration')
        Wizard = pool.get(
            'account.invoice.pay_using_transaction', type='wizard')

        transaction = create_payment_transaction()
        invoice = create_and_post_invoice(transaction.party)
        self.assertTrue(invoice)
        self.assertEqual(invoice.state, 'posted')
        self.assertTrue(invoice.amount_to_pay)

        company, = Company.search([])

        # Set the write-off configuration
        account_config = AccountConfiguration(1)
        account_config.write_off_threshold = Decimal('0.10')
        account_config.save()
        self.assertEqual(account_config.write_off_threshold, Decimal('0.10'))
        create_write_off()
        self.assertTrue(account_config.write_off)


        # Pay invoice using cash transaction
        with Transaction().set_context(active_id=invoice.id):
            pay_wizard = Wizard(Wizard.create()[0])
            defaults = pay_wizard.default_start()

            pay_wizard.start.invoice = defaults['invoice']
            pay_wizard.start.party = defaults['party']
            pay_wizard.start.company = defaults['company']
            pay_wizard.start.credit_account = defaults['credit_account']
            pay_wizard.start.owner = defaults['owner']
            pay_wizard.start.currency_digits = defaults['currency_digits']
            pay_wizard.start.amount = defaults['amount']
            pay_wizard.start.user = defaults['user']
            pay_wizard.start.gateway = transaction.gateway.id
            pay_wizard.start.payment_profile = None
            pay_wizard.start.reference = 'Test paying with cash'
            pay_wizard.start.method = transaction.gateway.method
            pay_wizard.start.transaction_type = defaults['transaction_type']

            with Transaction().set_context(company=company.id):
                pay_wizard.transition_pay()

        self.assertEqual(invoice.state, 'paid')
        self.assertEqual(AccountMove.search_count([]), 2)

        # There should be no journal entries on write-off journal
        self.assertEqual(AccountMove.search_count([
                    ('journal', '=', account_config.write_off.journal)
                    ]), 0)


def suite():
    suite = test_suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
            InvoicePaymentGatewayTestCase))
    return suite
