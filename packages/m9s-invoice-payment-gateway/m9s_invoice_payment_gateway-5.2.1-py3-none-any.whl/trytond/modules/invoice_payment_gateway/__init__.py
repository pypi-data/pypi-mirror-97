# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

from trytond.pool import Pool
from . import invoice

__all__ = ['register']


def register():
    Pool.register(
        invoice.Invoice,
        invoice.PaymentTransaction,
        invoice.PayInvoiceUsingTransactionStart,
        invoice.PayInvoiceUsingTransactionFailed,
        invoice.AccountConfiguration,
        module='invoice_payment_gateway', type_='model')
    Pool.register(
        invoice.PayInvoiceUsingTransaction,
        module='invoice_payment_gateway', type_='wizard')
