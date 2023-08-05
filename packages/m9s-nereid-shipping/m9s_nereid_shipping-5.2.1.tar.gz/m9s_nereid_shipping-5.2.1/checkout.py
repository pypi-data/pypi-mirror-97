# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
import json
from decimal import Decimal

from trytond.pool import Pool, PoolMeta
from trytond.exceptions import UserError
from trytond.modules.nereid_checkout.checkout import not_empty_cart, \
    sale_has_non_guest_party
from nereid import route, redirect, url_for, render_template, \
    request, flash, current_website
from trytond.modules.nereid_checkout.signals import cart_address_updated
from trytond.modules.nereid_cart_b2c.signals import cart_updated


class Cart(metaclass=PoolMeta):
    __name__ = 'nereid.cart'

    @cart_address_updated.connect
    @cart_updated.connect
    def delete_shipping_line(self):
        """
        Delete any shipping lines whenever the cart or address is being updated
        """
        pool = Pool()
        SaleLine = pool.get('sale.line')

        if not self.sale:
            return

        for line in self.sale.lines:
            if line.shipment_cost is not None:
                SaleLine.delete([line])


class Checkout(metaclass=PoolMeta):
    __name__ = 'nereid.checkout'

    @classmethod
    @route('/checkout/delivery-method', methods=['GET', 'POST'])
    @not_empty_cart
    @sale_has_non_guest_party
    def delivery_method(cls):
        '''
        Selection of delivery method (options)

        Based on the shipping address selected, the delivery options
        could be shown to the user. This may include choosing shipping speed
        and if there are multiple items, the option to choose items as they are
        available or all at once.
        '''
        pool = Pool()
        NereidCart = pool.get('nereid.cart')
        Carrier = pool.get('carrier')
        CarrierService = pool.get('carrier.service')
        Currency = pool.get('currency.currency')

        cart_sale = NereidCart.open_cart().sale

        if not cart_sale.shipment_address:
            return redirect(url_for('nereid.checkout.shipping_address'))

        if request.method == 'POST' and request.form.get('carrier_json'):
            rate = json.loads(request.form.get('carrier_json'))
            rate.update({
                'carrier': Carrier(rate['carrier']),
                'carrier_service': CarrierService(rate['carrier_service']),
                'cost_currency': Currency(rate['cost_currency']),
                'cost': Decimal("%s" % (rate['cost'], ))
            })
            cart_sale.apply_shipping_rate(rate)
            return redirect(url_for('nereid.checkout.payment_method'))

        delivery_rates = []
        try:
            delivery_rates = cart_sale.get_shipping_rates(
                current_website.carriers,
                silent=True
            )
        except UserError as e:
            # Possible Errors: Overweighted shipment, Invalid address
            # TODO: Handle gracefully
            flash(e.message)
            return redirect(url_for('nereid.checkout.shipping_address'))

        return render_template(
            'checkout/delivery_method.jinja', delivery_rates=delivery_rates,
            sale=cart_sale)
