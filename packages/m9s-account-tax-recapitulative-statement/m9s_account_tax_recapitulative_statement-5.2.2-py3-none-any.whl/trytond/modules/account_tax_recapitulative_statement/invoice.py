# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import PoolMeta


class InvoiceLine(metaclass=PoolMeta):
    __name__ = 'account.invoice.line'

    def _compute_taxes(self):
        tax_lines = super(InvoiceLine, self)._compute_taxes()
        for line in tax_lines:
            if line.tax.vat_code_required:
                line.vat_code = self.party.vat_code if self.party else \
                        self.invoice.party.vat_code
        return tax_lines


class InvoiceTax(metaclass=PoolMeta):
    __name__ = 'account.invoice.tax'

    def get_move_line(self):
        line = super(InvoiceTax, self).get_move_line()
        if self.tax_code and self.tax.vat_code_required:
            tax_line = line[0].tax_lines[0]
            tax_line.vat_code = self.invoice.party.vat_code
        return line
