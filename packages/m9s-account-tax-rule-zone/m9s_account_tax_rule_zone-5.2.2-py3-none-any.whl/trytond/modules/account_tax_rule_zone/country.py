# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
from trytond.model import ModelView, ModelSQL, fields
from trytond.pool import Pool, PoolMeta
from trytond.pyson import Eval
from trytond import backend


class Country(metaclass=PoolMeta):
    __name__ = 'country.country'
    tax_zone = fields.Many2One('account.tax.zone', 'Tax Zone')
