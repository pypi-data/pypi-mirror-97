# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import PoolMeta
from trytond.model import fields
from trytond.pyson import Bool, Eval


class Website(metaclass=PoolMeta):
    "Define the credit card handler"
    __name__ = 'nereid.website'

    accept_credit_card = fields.Boolean('Accept Credit Card')
    save_payment_profile = fields.Boolean(
        'Allow Saving Payment Profiles', states={
            'invisible': ~Bool(Eval('accept_credit_card'))
        }, depends=['accept_credit_card']
    )
    credit_card_gateway = fields.Many2One(
        'payment_gateway.gateway', 'Credit Card Gateway',
        states={
            'required': Bool(Eval('accept_credit_card')),
            'invisible': ~Bool(Eval('accept_credit_card'))
        }, depends=['accept_credit_card'],
        domain=[('method', 'in', ['credit_card', 'dummy'])]
    )
    instructions = fields.Text('Credit Card Instructions', translate=True)
