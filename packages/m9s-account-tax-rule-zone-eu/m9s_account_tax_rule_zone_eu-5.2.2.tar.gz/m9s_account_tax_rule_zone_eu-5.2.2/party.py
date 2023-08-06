# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta


class Party(metaclass=PoolMeta):
    __name__ = 'party.party'
    legal_form = fields.Function(fields.Char('Legal Form'),
        'get_legal_form')

    def get_legal_form(self, name):
        vat_code = [i for i in self.identifiers if i.type == 'eu_vat']
        if vat_code or self.party_type == 'organization':
            return 'company'
        else:
            return 'person'
