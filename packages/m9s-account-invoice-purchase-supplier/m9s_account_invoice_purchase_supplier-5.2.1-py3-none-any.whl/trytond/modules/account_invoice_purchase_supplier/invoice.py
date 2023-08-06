# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from decimal import Decimal
from trytond.model import fields
from trytond.pool import PoolMeta, Pool
from trytond.transaction import Transaction
from trytond.config import config

discount_digits = (16, config.getint('product', 'discount_decimal',
    default=4))


class InvoiceLine(metaclass=PoolMeta):
    __name__ = 'account.invoice.line'

    def _get_context_invoice_price(self):
        context = {}
        if getattr(self, 'invoice', None):
            if getattr(self.invoice, 'currency', None):
                context['currency'] = self.invoice.currency.id
            if getattr(self.invoice, 'party', None):
                context['supplier'] = self.invoice.party.id
            if getattr(self.invoice, 'invoice_date', None):
                context['invoice_date'] = self.invoice.invoice_date
        if self.unit:
            context['uom'] = self.unit.id
        else:
            context['uom'] = self.product.purchase_uom.id
        context['taxes'] = [t.id for t in self.taxes]
        return context

    def get_supplier_price(self):
        pool = Pool()
        Uom = pool.get('product.uom')
        ProductSupplier = pool.get('purchase.product_supplier')
        ProductSupplierPrice = pool.get('purchase.product_supplier.price')

        context = Transaction().context

        if context.get('uom'):
            uom = Uom(context['uom'])
        else:
            uom = self.product.default_uom

        gross_unit_price = gross_unit_price_wo_round = self.gross_unit_price
        unit_price = self.gross_unit_price
        discount = Decimal(0)

        with Transaction().set_context(self._get_context_invoice_price()):
            pattern = ProductSupplier.get_pattern()
            for product_supplier in self.product.product_suppliers:
                if product_supplier.match(pattern):
                    pattern = ProductSupplierPrice.get_pattern()
                    for price in product_supplier.prices:
                        if price.match(self.quantity, uom, pattern):
                            discount = price.discount or Decimal(0)
                            gross_unit_price_wo_round = price.gross_unit_price
                            unit_price = price.unit_price
                            break
                    break

        if unit_price is not None:
            digits = self.__class__.unit_price.digits[1]
            unit_price = unit_price.quantize(Decimal(str(10.0 ** -digits)))

        if gross_unit_price is not None:
            digits = self.__class__.gross_unit_price.digits[1]
            gross_unit_price = gross_unit_price_wo_round.quantize(
                Decimal(str(10.0 ** -digits)))

        self.gross_unit_price = gross_unit_price
        self.gross_unit_price_wo_round = gross_unit_price_wo_round
        self.unit_price = unit_price
        self.discount = discount

    @fields.depends('invoice', 'quantity', 'product', 'gross_unit_price')
    def on_change_product(self):
        super(InvoiceLine, self).on_change_product()
        if getattr(self, 'invoice', None):
            if self.invoice.type == 'in' and self.product and self.quantity:
                self.get_supplier_price()
