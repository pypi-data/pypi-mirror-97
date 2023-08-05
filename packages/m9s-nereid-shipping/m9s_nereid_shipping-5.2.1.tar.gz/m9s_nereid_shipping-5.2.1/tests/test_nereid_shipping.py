# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
import unittest
import pycountry
import json

from decimal import Decimal
from ast import literal_eval
from unittest.mock import patch
from datetime import date

from trytond.tests.test_tryton import suite as test_suite
from trytond.tests.test_tryton import with_transaction
from trytond.pool import Pool
from trytond.transaction import Transaction
from trytond.config import config

from nereid.testing import NereidModuleTestCase

from trytond.modules.company.tests import create_company, set_company
from trytond.modules.nereid.tests.test_common import (create_website_locale,
    create_static_file)
from trytond.modules.payment_gateway.tests import (create_payment_gateway,
    create_payment_profile)
from trytond.modules.nereid_cart_b2c.tests import (create_website,
    create_countries, create_pricelists, create_product_template)

config.set('database', 'path', '/tmp')


class NereidShippingTestCase(NereidModuleTestCase):
    'Test Nereid Shipping module'
    module = 'nereid_shipping'

    def setUp(self):
        self.templates = {
            'home.jinja': '{{get_flashed_messages()}}',
            'login.jinja':
                '{{ login_form.errors }} {{get_flashed_messages()}}',
            'shopping-cart.jinja':
                'Cart:{{ cart.id }},{{get_cart_size()|round|int}},'
                '{{cart.sale.total_amount}}',
            'product.jinja':
                '{{ product.sale_price(product.id) }}',
            'address-edit.jinja':
            'Address Edit {% if address %}ID:{{ address.id }}{% endif %}'
            '{{ form.errors }}',
            'address.jinja': '',
            'checkout/signin.jinja': '{{form.errors|safe}}',
            'checkout/signin-email-in-use.jinja': '{{email}} in use',
            'checkout/shipping_address.jinja': '{{address_form.errors|safe}}',
            'checkout/billing_address.jinja': '{{address_form.errors|safe}}',
            'checkout/payment_method.jinja': '''[
                {{payment_form.errors|safe}},
                {{credit_card_form.errors|safe}},
            ]''',
            'emails/sale-confirmation-text.jinja': ' ',
            'emails/sale-confirmation-html.jinja': ' ',
            'checkout.jinja': '{{form.errors|safe}}',
            'sale.jinja': ' ',
            'sales.jinja': '''{{request.args.get('filter_by')}}
                {% for sale in sales %}#{{sale.id}}{% endfor %}
            '''
            }

        # Patch SMTP Lib
        self.smtplib_patcher = patch('smtplib.SMTP')
        self.PatchedSMTP = self.smtplib_patcher.start()

    def tearDown(self):
        # Unpatch SMTP Lib
        self.smtplib_patcher.stop()

    # ##################################
    # 000 Test the Delivery Method Step
    # ##################################

    @with_transaction()
    def test_0005_guest_no_skip_signin(self):
        '''
        Ensure that guest orders cant directly skip to enter shipping address
        '''
        # Setup defaults
        # A gateway sets up a lot of configuration stuff (fiscalyear, chart,
        # etc.)
        website = create_website()
        website.save()
        gateway = create_payment_gateway()
        gateway.save()

        # Create product templates with products
        template1, = create_product_template(
            'product-1',
            [{
                'type': 'goods',
                'salable': True,
                'list_price': Decimal('10'),
            }],
            uri='product-1',
        )

        product1 = template1.products[0]
        quantity = 5

        app = self.get_app()
        with app.test_client() as c:
            c.post('/en/cart/add',
                data={
                    'product': product1.id,
                    'quantity': quantity,
                    })
            rv = c.get('/en/checkout/delivery-method')
            self.assertEqual(rv.status_code, 302)
            self.assertTrue(
                rv.location.endswith('/en/checkout/sign-in'))

    @with_transaction()
    def test_0010_guest_signedin_no_skip_shipping_address(self):
        '''
        Ensure that guest orders cant directly skip to enter shipping address
        Ensure that no delivery method selection if no shipment weight
        '''
        pool = Pool()
        Country = pool.get('country.country')

        # Setup defaults
        # A gateway sets up a lot of configuration stuff (fiscalyear, chart,
        # etc.)
        website = create_website()
        website.save()
        gateway = create_payment_gateway()
        gateway.save()

        # Create product templates with products
        template1, = create_product_template(
            'product-1',
            [{
                'type': 'goods',
                'salable': True,
                'list_price': Decimal('10'),
            }],
            uri='product-1',
        )

        product1 = template1.products[0]
        quantity = 5

        create_countries()
        countries = Country.search([])
        website.countries = countries
        website.save()
        country = countries[0]
        subdivision = country.subdivisions[0]

        app = self.get_app()
        with app.test_client() as c:
            c.post('/en/cart/add',
                data={
                    'product': product1.id,
                    'quantity': quantity,
                    })

            # Sign-in
            rv = c.post('/en/checkout/sign-in',
                data={
                    'email': 'new@example.com',
                    'checkout_mode': 'guest',
                })

            # Redirect to shipping address since there is no address
            # and shipment method can't be selected without a delivery
            # address
            rv = c.get('/en/checkout/delivery-method')
            self.assertEqual(rv.status_code, 302)
            self.assertTrue(
                rv.location.endswith('/en/checkout/shipping-address'))

            # Shipping address page gets rendered
            rv = c.post('/en/checkout/shipping-address',
                data={
                    'name': 'Max Mustermann',
                    'street': 'Musterstr. 26',
                    'zip': '79852',
                    'city': 'Musterstadt',
                    'country': country.id,
                    'subdivision': subdivision.id,
                })
            self.assertEqual(rv.status_code, 302)


def suite():
    suite = test_suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
            NereidShippingTestCase))
    return suite
