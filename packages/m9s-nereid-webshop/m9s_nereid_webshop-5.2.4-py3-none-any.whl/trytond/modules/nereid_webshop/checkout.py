# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from decimal import Decimal
from wtforms import StringField
from nereid import url_for, flash, redirect
from trytond.pool import Pool, PoolMeta
from trytond.transaction import Transaction
from werkzeug.wrappers import BaseResponse
from trytond.modules.nereid_checkout.checkout import PaymentForm
from nereid.contrib.locale import make_lazy_gettext

_ = make_lazy_gettext('nereid_webshop')


class GiftCardPaymentForm(PaymentForm):
    '''
    Form to capture additional payment data

    inherited from nereid_checkout
    '''
    gift_card_number = StringField(_('Gift Card Number'))


class Checkout(metaclass=PoolMeta):
    __name__ = 'nereid.checkout'

    @classmethod
    def get_form_payment(cls):
        '''
        Return a payment form
        '''
        return GiftCardPaymentForm()

    @classmethod
    def _process_payment(cls, cart):
        pool = Pool()
        PaymentMethod = pool.get('nereid.website.payment_method')
        GiftCard = pool.get('gift_card.gift_card')

        payment_form = cls.get_payment_form()

        if payment_form.alternate_payment_method.data:
            payment_method = PaymentMethod(
                    payment_form.alternate_payment_method.data)
            if payment_method.method == 'gift_card':
                gift_cards = GiftCard.search([
                        ('number', '=', payment_form.gift_card_number.data),
                        ('state', '=', 'active'),
                        ], limit=1)
                if not gift_cards:
                    flash(
                        _('No active gift card certificate '
                            'found for the given number.'),
                        'Error')
                    return redirect(url_for('nereid.checkout.payment_method'))
                gift_card = gift_cards[0]
                with Transaction().set_context(gift_card=gift_card.id):

                    # Only one payment per gateway and gift_card
                    gateway = payment_method.gateway
                    sale = cart.sale
                    rv = None
                    payment = sale._get_payment_for_gateway(gateway)
                    if payment is None:
                        rv = sale._add_sale_payment(
                            alternate_payment_method=payment_method)
                        payment = sale._get_payment_for_gateway(gateway)
                    # Update the paymount_amount with the actual needed sum,
                    # when it was set to 0 by a cancelation.
                    if payment.amount == Decimal('0'):
                        payment.amount = sale._get_amount_to_checkout()
                        payment.save()
                    payment_transaction = payment._create_payment_transaction(
                        payment.amount, str(_('Paid by Gift Card')))
                    payment_transaction.save()
                    payment.authorize()
                    if isinstance(rv, BaseResponse):
                        # If the alternate payment method introduced a
                        # redirect, then save the order and go to that
                        cls.confirm_cart(cart)
                        return rv
                    amount_to_pay = cart.sale._get_amount_to_checkout()
                    if amount_to_pay <= 0:
                        return cls.confirm_cart(cart)
                    flash(_('Payment by Gift Card with amount '
                            '%(amount)s registered.', amount=payment.amount))
                    return redirect(url_for('nereid.checkout.payment_method'))

        return super(Checkout, cls)._process_payment(cart)
