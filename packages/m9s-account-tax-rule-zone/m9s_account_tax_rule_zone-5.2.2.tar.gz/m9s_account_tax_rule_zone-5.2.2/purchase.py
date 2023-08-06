# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import PoolMeta
from trytond.model import fields
from trytond.pyson import Eval


class Purchase(metaclass=PoolMeta):
    __name__ = 'purchase.purchase'

    @classmethod
    def __setup__(cls):
        super(Purchase, cls).__setup__()
        for field in (cls.invoice_address, cls.warehouse):
            field.states['readonly'] |= (
                Eval('lines', [0]) & Eval('invoice_address'))
            field.depends.extend(['invoice_address'])


class PurchaseLine(metaclass=PoolMeta):
    __name__ = 'purchase.line'

    def _get_tax_rule_pattern(self):
        pattern = super(PurchaseLine, self)._get_tax_rule_pattern()

        from_zone, to_zone = None, None
        if self.purchase:
            if self.purchase.invoice_address:
                from_zone = self.purchase.invoice_address.country.tax_zone
            warehouse = self.purchase.warehouse
            if warehouse and warehouse.address:
                to_zone = warehouse.address.country.tax_zone

        pattern['from_zone'] = from_zone.id if from_zone else None
        pattern['to_zone'] = to_zone.id if to_zone else None
        return pattern

    @fields.depends('_parent_purchase.warehouse',
        '_parent_purchase.invoice_address')
    def on_change_product(self):
        super(PurchaseLine, self).on_change_product()
