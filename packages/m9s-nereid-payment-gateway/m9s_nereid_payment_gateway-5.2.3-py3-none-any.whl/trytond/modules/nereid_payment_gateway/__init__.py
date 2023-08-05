# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool
from . import party
from . import website

__all__ = ['register']


def register():
    Pool.register(
        party.Party,
        party.PaymentProfile,
        website.Website,
        module='nereid_payment_gateway', type_='model')
