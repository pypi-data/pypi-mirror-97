# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool
from . import invoice
from . import tax


__all__ = ['register']


def register():
    Pool.register(
        tax.Line,
        tax.Tax,
        tax.TaxTemplate,
        module='account_tax_recapitulative_statement', type_='model')
    Pool.register(
        invoice.InvoiceLine,
        invoice.InvoiceTax,
        depends=['account_invoice'],
        module='account_tax_recapitulative_statement', type_='model')
