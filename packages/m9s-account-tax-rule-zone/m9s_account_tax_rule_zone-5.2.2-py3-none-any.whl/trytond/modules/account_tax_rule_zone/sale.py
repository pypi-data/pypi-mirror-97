# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool, PoolMeta
from trytond.model import fields
from trytond.pyson import Eval


class Sale(metaclass=PoolMeta):
    __name__ = 'sale.sale'

    @classmethod
    def __setup__(cls):
        super(Sale, cls).__setup__()
        for field in (cls.shipment_party, cls.shipment_address, cls.warehouse):
            field.states['readonly'] |= (
                Eval('lines', [0]) & Eval('shipment_address'))
            field.depends.extend(['shipment_address'])


class SaleLine(metaclass=PoolMeta):
    __name__ = 'sale.line'

    def _get_tax_rule_pattern(self):
        pool = Pool()
        Location = pool.get('stock.location')

        pattern = super(SaleLine, self)._get_tax_rule_pattern()

        from_zone, to_zone = None, None
        if self.id is None or self.id < 0:
            warehouse = self.get_warehouse('warehouse')
            if warehouse:
                warehouse = Location(warehouse)
        else:
            warehouse = self.warehouse
        if warehouse and warehouse.address:
            from_zone = warehouse.address.country.tax_zone
        elif self.sale:
            from_zone = self.sale.company.party.address_get('delivery')
        if self.sale and self.sale.shipment_address:
            to_zone = self.sale.shipment_address.country.tax_zone

        pattern['from_zone'] = from_zone.id if from_zone else None
        pattern['to_zone'] = to_zone.id if to_zone else None
        return pattern

    @fields.depends('_parent_sale.warehouse', '_parent_sale.shipment_address')
    def on_change_product(self):
        super(SaleLine, self).on_change_product()
