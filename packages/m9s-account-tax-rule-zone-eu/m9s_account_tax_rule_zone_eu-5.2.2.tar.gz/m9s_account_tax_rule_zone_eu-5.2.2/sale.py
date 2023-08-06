# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import PoolMeta
from trytond.model import fields

from .account import TYPES


class SaleLine(metaclass=PoolMeta):
    __name__ = 'sale.line'

    def _get_tax_rule_pattern(self):

        pattern = super(SaleLine, self)._get_tax_rule_pattern()

        type, legal_form = None, None
        if (self.product and
                self.product.type in [i[0] for i in TYPES]):
            type = self.product.type
        if self.sale and self.sale.party:
            legal_form = self.sale.party.legal_form

        pattern['type'] = type
        pattern['legal_form'] = legal_form
        return pattern
