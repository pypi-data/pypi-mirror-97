# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

try:
    from trytond.modules.account_invoice_purchase_supplier.tests.test_account_invoice_purchase_supplier import suite
except ImportError:
    from .test_account_invoice_purchase_supplier import suite

__all__ = ['suite']
