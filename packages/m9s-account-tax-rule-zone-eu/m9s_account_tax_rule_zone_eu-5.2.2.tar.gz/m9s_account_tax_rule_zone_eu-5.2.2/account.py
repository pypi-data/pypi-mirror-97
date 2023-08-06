# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool, PoolMeta
from trytond.model import fields
from trytond.transaction import Transaction


TYPES = [
    (None, ''),
    ('goods', 'Goods'),
    ('service', 'Services'),
    ]
LEGAL_FORMS = [
    (None, ''),
    ('person', 'Person (without VAT ID)'),
    ('company', 'Company (with VAT ID)'),
    ]


class TaxRuleLineTemplate(metaclass=PoolMeta):
    __name__ = 'account.tax.rule.line.template'
    type = fields.Selection(TYPES, 'Type')
    legal_form = fields.Selection(LEGAL_FORMS,
        'Legal Form of Party (VAT Specification)')
    comment = fields.Char('Comment')

    def _get_tax_rule_line_value(self, rule_line=None):
        value = super(TaxRuleLineTemplate, self)._get_tax_rule_line_value(
            rule_line=rule_line)
        if not rule_line or rule_line.type != self.type:
            value['type'] = (
                self.type if self.type else None)
        if not rule_line or rule_line.legal_form != self.legal_form:
            value['legal_form'] = (
                self.legal_form if self.legal_form else None)
        if not rule_line or rule_line.comment != self.comment:
            value['comment'] = (
                self.comment if self.comment else None)
        return value


class TaxRuleLine(metaclass=PoolMeta):
    __name__ = 'account.tax.rule.line'
    type = fields.Selection(TYPES, 'Type')
    legal_form = fields.Selection(LEGAL_FORMS,
            'Legal Form of Party (VAT Specification)')
    comment = fields.Char('Comment')


class InvoiceLine(metaclass=PoolMeta):
    __name__ = 'account.invoice.line'

    def _get_tax_rule_pattern(self):
        pool = Pool()
        try:
            SaleLine = pool.get('sale.line')
        except KeyError as e:
            SaleLine = None
        try:
            PurchaseLine = pool.get('purchase.line')
        except KeyError as e:
            PurchaseLine = None
        try:
            Work = pool.get('project.work')
        except KeyError as e:
            Work = None

        pattern = super(InvoiceLine, self)._get_tax_rule_pattern()

        type, legal_form = None, None
        if (self.product and
                self.product.type in [i[0] for i in TYPES]):
            type = self.product.type
        if SaleLine and isinstance(self.origin, SaleLine):
            legal_form = self.origin.sale.shipment_address.party.legal_form
        elif PurchaseLine and isinstance(self.origin, PurchaseLine):
            legal_form = self.origin.purchase.invoice_address.party.legal_form
        elif Work and isinstance(self.origin, Work):
            legal_form = self.origin.party.legal_form
        else:
            legal_form = self.invoice.party.legal_form

        pattern['type'] = type
        pattern['legal_form'] = legal_form
        return pattern
