# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import PoolMeta

from .account import TYPES


class CreatePurchase(metaclass=PoolMeta):
    __name__ = 'purchase.request.create_purchase'

    @classmethod
    def _get_tax_rule_pattern(cls, line, purchase):
        pattern = super(CreatePurchase, cls)._get_tax_rule_pattern(line,
            purchase)

        type, legal_form = None, None
        product = line.product
        if product and product.type in [i[0] for i in TYPES]:
            type = product.type
        party = purchase.party
        if party:
            legal_form = party.legal_form

        pattern['type'] = type
        pattern['legal_form'] = legal_form
        return pattern
