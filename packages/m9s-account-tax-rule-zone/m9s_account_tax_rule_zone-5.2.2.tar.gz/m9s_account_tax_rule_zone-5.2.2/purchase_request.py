# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import PoolMeta


class CreatePurchase(metaclass=PoolMeta):
    __name__ = 'purchase.request.create_purchase'

    @classmethod
    def _get_tax_rule_pattern(cls, line, purchase):
        pattern = super(CreatePurchase, cls)._get_tax_rule_pattern(line,
            purchase)

        from_zone, to_zone = None, None
        party = purchase.party
        if party:
            address = party.address_get('invoice')
            from_zone = address.country.tax_zone
        warehouse = purchase.warehouse
        if warehouse and warehouse.address:
            to_zone = warehouse.address.country.tax_zone

        pattern['from_zone'] = from_zone.id if from_zone else None
        pattern['to_zone'] = to_zone.id if to_zone else None
        return pattern
