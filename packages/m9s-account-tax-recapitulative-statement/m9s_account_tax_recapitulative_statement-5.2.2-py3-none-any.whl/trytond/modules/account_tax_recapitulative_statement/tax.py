# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import logging
from trytond.model import fields
from trytond.pool import PoolMeta
from trytond.exceptions import UserError
from trytond.i18n import gettext

HAS_VATNUMBER = False
try:
    import vatnumber
    HAS_VATNUMBER = True
except ImportError:
    logging.getLogger(__name__).warning(
            'Unable to import vatnumber. VAT number validation disabled.')


class TaxTemplate(metaclass=PoolMeta):
    __name__ = 'account.tax.template'

    vat_code_required = fields.Boolean('Vat Code Required')

    def _get_tax_value(self, tax=None):
        res = super(TaxTemplate, self)._get_tax_value(tax=tax)
        field = 'vat_code_required'
        if not tax or getattr(tax, field) != getattr(self, field):
            res[field] = getattr(self, field)
        return res

    @classmethod
    def validate(cls, taxes):
        super(TaxTemplate, cls).validate(taxes)
        for tax in taxes:
            tax.check_vat_code_required()

    def check_vat_code_required(self):
        taxes = self.search([
                ('vat_code_required', '!=', self.vat_code_required),
                ['OR',
                    ('id' , 'in', [t.id for t in self.childs]),
                    ('parent', '=', self.id)
                    ],
                ])
        if taxes:
            raise UserError(gettext(
                    'account_tax_recapitulative_statement.same_vat_code_required',
                    first=self.rec_name, second=taxes[0].rec_name,))


class Tax(metaclass=PoolMeta):
    __name__ = 'account.tax'

    vat_code_required = fields.Boolean('Vat Code Required')


class Line(metaclass=PoolMeta):
    __name__ = 'account.tax.line'

    vat_code = fields.Char('VAT Code',
            # TODO: Add tax.vat_code_required as function field
            # #states={
            #'required': Eval('tax.vat_code_required') == Bool(True),
            #    }
            )

    @fields.depends('tax', 'move_line')
    def on_change_tax(self):
        try:
            super().on_change_tax()
        except:
            pass

        self.vat_code = None
        if self.tax:
            if self.tax.vat_code_required:
                if self.move_line.party and self.move_line.party.vat_code:
                    self.vat_code = self.move_line.party.vat_code

    @classmethod
    def validate(cls, lines):
        super(Line, cls).validate(lines)
        for line in lines:
            line.check_vat_code()

    def check_vat_code(self):
        if self.tax.vat_code_required and not self.vat_code:
            raise UserError(gettext(
                    'account_tax_recapitulative_statement.missing_line_vat_code',
                    line=self.id))
            self.move_line.party.check_vat()

    @classmethod
    def _set_vat_code(cls, lines):
        '''
        Check and set the vat code according to the used taxes.
        '''
        for line in lines:
            if line.tax:
                if line.tax.vat_code_required and not line.vat_code:
                    if not line.move_line.party:
                        raise UserError(gettext(
                                'account_tax_recapitulative_statement.missing_party_move_line'))
                    if not line.move_line.party.vat_code:
                        raise UserError(gettext(
                                'account_tax_recapitulative_statement.missing_party_vat_code',
                                party=line.move_line.party.rec_name))
                    line.move_line.party.check_vat()
                    cls.write([line.id], {
                            'vat_code': line.move_line.party.vat_code,
                            })

    @classmethod
    def create(cls, vlist):
        lines = super(Line, cls).create(vlist)
        cls._set_vat_code(lines)
        return lines

    @classmethod
    def write(cls, *args):
        super(Line, cls).write(*args)
        lines = sum(args[::2], [])
        cls._set_vat_code(lines)
