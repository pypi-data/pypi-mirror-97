# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool
from . import account
from . import country
from . import sale
from . import purchase
from . import purchase_request

__all__ = ['register']


def register():
    Pool.register(
        country.Country,
        account.TaxZone,
        account.TaxRuleLineTemplate,
        account.TaxRuleLine,
        module='account_tax_rule_zone', type_='model')
    Pool.register(
        account.InvoiceLine,
        depends=['account_invoice', 'project_invoice'],
        module='account_tax_rule_zone', type_='model')
    Pool.register(
        sale.Sale,
        sale.SaleLine,
        depends=['sale'],
        module='account_tax_rule_zone', type_='model')
    Pool.register(
        purchase.PurchaseLine,
        depends=['purchase'],
        module='account_tax_rule_zone', type_='model')
    Pool.register(
        purchase_request.CreatePurchase,
        depends=['purchase_request'],
        module='account_tax_rule_zone', type_='wizard')
