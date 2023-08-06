# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

try:
    from trytond.modules.invoice_payment_gateway.tests.test_invoice_payment_gateway import (
        suite, create_write_off, create_payment_term, create_products,
        create_and_post_invoice)
except ImportError:
    from .test_invoice_payment_gateway import (
        suite, create_write_off, create_payment_term, create_products,
        create_and_post_invoice)

__all__ = ['suite', 'create_write_off', 'create_payment_term',
    'create_products', 'create_and_post_invoice']

