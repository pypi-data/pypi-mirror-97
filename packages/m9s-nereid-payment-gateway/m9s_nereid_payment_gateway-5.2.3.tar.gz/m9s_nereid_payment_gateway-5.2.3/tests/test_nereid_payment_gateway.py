# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
import unittest
import json
import pycountry

from decimal import Decimal

from trytond.tests.test_tryton import suite as test_suite
from trytond.tests.test_tryton import with_transaction
from trytond.pool import Pool
from trytond.exceptions import UserError
from trytond.transaction import Transaction

from nereid.testing import NereidModuleTestCase
from nereid import current_user, current_website

from trytond.modules.nereid.tests.test_common import (create_website,
    create_static_file)
from trytond.modules.payment_gateway.tests import (create_payment_gateway,
    create_payment_profile)

from trytond.config import config
config.set('database', 'path', '/tmp')


def create_countries(count=5):
    """
    Create some sample countries and subdivisions
    """
    pool = Pool()
    Subdivision = pool.get('country.subdivision')
    Country = pool.get('country.country')

    for country in list(pycountry.countries)[0:count]:
        countries = Country.create([{
            'name': country.name,
            'code': country.alpha_2,
        }])
        try:
            divisions = pycountry.subdivisions.get(
                country_code=country.alpha_2
            )
        except KeyError:
            pass
        else:
            for subdivision in list(divisions)[0:count]:
                Subdivision.create([{
                    'country': countries[0].id,
                    'name': subdivision.name,
                    'code': subdivision.code,
                    'type': subdivision.type.lower(),
                }])


class NereidPaymentGatewayTestCase(NereidModuleTestCase):
    'Test Nereid Payment Gateway module'
    module = 'nereid_payment_gateway'

    def setUp(self):
        self.templates = {
            'home.jinja': '{{get_flashed_messages()}}',
            'login.jinja':
            '{{ login_form.errors }} {{get_flashed_messages()}}',
            'my-cards.jinja':
                '{{ current_user.party.payment_profiles| length }}',
            'add-card.jinja':
            '''
            {% for error in form.address.errors %}
                {{ error }}
            {% endfor %}
            ''',
            }

    @with_transaction()
    def test_0010_add_payment_profile(self):
        """
        Test to add a new payment profile.
        """
        pool = Pool()
        Party = pool.get('party.party')
        Address = pool.get('party.address')
        Country = pool.get('country.country')
        Company = pool.get('company.company')
        NereidUser = pool.get('nereid.user')
        Website = pool.get('nereid.website')

        create_website()
        app = self.get_app()

        # Create test users
        party, = Party.create([{
            'name': 'Registered User',
        }])
        company, = Company.search([])
        registered_user, = NereidUser.create([{
            'party': party,
            'name': 'Registered User',
            'email': 'email@example.com',
            'password': 'password',
            'company': company,
        }])
        # Define a new payment gateway
        gateway = create_payment_gateway(method='dummy')
        website, = Website.search([])
        website.credit_card_gateway = gateway
        website.save()

        with app.test_client() as c:
            response = c.post(
                '/en/login',
                data={
                    'email': 'email@example.com',
                    'password': 'password',
                    }
                )
            self.assertEqual(response.status_code, 302)  # Login success

            create_countries()
            available_countries = Country.search([], limit=5)
            address, = Address.create([{
                'party': party,
                'name': 'Name',
                'street': 'Street',
                'zip': 'zip',
                'city': 'City',
                'country': available_countries[0].id,
                'subdivision':
                    available_countries[0].subdivisions[0].id,
            }])
            self.assertEqual(
                len(current_user.party.payment_profiles), 0)

            with Transaction().set_context({'dummy_succeed': True}):
                rv = c.post(
                    '/en/my-cards/add-card',
                    data={
                        'owner': 'Test User 1',
                        'number': '4111111111111111',
                        'expiry_month': '01',
                        'expiry_year': '2025',
                        'cvv': '123',
                        'address': address.id,
                        }
                    )
                self.assertEqual(
                    len(current_user.party.payment_profiles), 1)

                ## Test to handle xhr request
                #rv = c.post(
                #    '/en/my-cards/add-card',
                #    data={
                #        'owner': 'Test User 2',
                #        'number': '4111111111111111',
                #        'expiry_month': '05',
                #        'expiry_year': '2020',
                #        'cvv': '111',
                #        'address': address.id,
                #        }, headers=[('X-Requested-With', 'XMLHttpRequest')]
                #    )

                #self.assertEqual(
                #    len(current_user.party.payment_profiles), 2)
                #self.assertEqual(rv.status_code, 200)

    @with_transaction()
    def test_0020_view_payment_profiles(self):
        """
        Test to retreive stored credit card profiles.
        """
        pool = Pool()
        Party = pool.get('party.party')
        Address = pool.get('party.address')
        Country = pool.get('country.country')
        Company = pool.get('company.company')
        NereidUser = pool.get('nereid.user')
        Website = pool.get('nereid.website')
        Profile = pool.get('party.payment_profile')
        Gateway = pool.get('payment_gateway.gateway')
        Journal = pool.get('account.journal')

        create_website()
        app = self.get_app()

        # Create test users
        party, = Party.create([{
            'name': 'Registered User',
        }])
        company, = Company.search([])
        registered_user, = NereidUser.create([{
            'party': party,
            'name': 'Registered User',
            'email': 'email@example.com',
            'password': 'password',
            'company': company,
        }])
        # Define a new payment gateway
        gateway = create_payment_gateway(method='dummy')
        website, = Website.search([])
        website.credit_card_gateway = gateway
        website.save()

        with app.test_client() as c:
            response = c.post(
                '/en/login',
                data={
                    'email': 'email@example.com',
                    'password': 'password',
                    }
                )
            self.assertEqual(response.status_code, 302)  # Login success

            create_countries()
            available_countries = Country.search([], limit=5)
            address, = Address.create([{
                'party': party,
                'name': 'Name',
                'street': 'Street',
                'zip': 'zip',
                'city': 'City',
                'country': available_countries[0].id,
                'subdivision':
                    available_countries[0].subdivisions[0].id,
            }])
            self.assertEqual(
                len(current_user.party.payment_profiles), 0)

            rv = c.get('/en/my-cards')
            self.assertEqual(rv.data.decode('utf-8'), '0')

            profile, = Profile.create([{
                'last_4_digits': '1111',
                'sequence': '10',
                'expiry_month': '01',
                'expiry_year': '2018',
                'address': address.id,
                'party': current_user.party.id,
                'provider_reference': '27478839|25062702',
                'gateway': gateway.id,
            }])

            with Transaction().set_context({'dummy_succeed': True}):
                rv = c.get('/en/my-cards')
                self.assertEqual(rv.data.decode('utf-8'), '1')

            profile, = Profile.create([{
                'last_4_digits': '1131',
                'sequence': '10',
                'expiry_month': '02',
                'expiry_year': '2018',
                'address': address.id,
                'party': current_user.party.id,
                'provider_reference': '27478839|25062710',
                'gateway': gateway.id,
            }])

            with Transaction().set_context({'dummy_succeed': True}):
                rv = c.get('/en/my-cards')
                self.assertEqual(rv.data.decode('utf-8'), '2')

            # Test to handel xhr request
            rv = c.get(
                '/en/my-cards',
                headers=[('X-Requested-With', 'XMLHttpRequest')]
            )
            json_data = json.loads(rv.data)['payment_profile']

            self.assertEqual(len(json_data), 2)
            self.assertEqual(json_data[0]['last_4_digits'], '1111')
            self.assertEqual(json_data[1]['last_4_digits'], '1131')

    @with_transaction()
    def test_0040_add_card_with_invalid_address(self):
        """
        Test for user trying to add card with invalid billing address.
        """
        pool = Pool()
        Party = pool.get('party.party')
        Address = pool.get('party.address')
        Country = pool.get('country.country')
        Company = pool.get('company.company')
        NereidUser = pool.get('nereid.user')
        Website = pool.get('nereid.website')

        create_website()
        app = self.get_app()

        # Create test users
        party, = Party.create([{
            'name': 'Registered User',
        }])
        company, = Company.search([])
        registered_user, = NereidUser.create([{
            'party': party,
            'name': 'Registered User',
            'email': 'email@example.com',
            'password': 'password',
            'company': company,
        }])
        # Define a new payment gateway
        gateway = create_payment_gateway(method='dummy')
        website, = Website.search([])
        website.credit_card_gateway = gateway
        website.save()

        with app.test_client() as c:
            response = c.post(
                '/en/login',
                data={
                    'email': 'email@example.com',
                    'password': 'password',
                    }
                )
            self.assertEqual(response.status_code, 302)  # Login success

            create_countries()
            available_countries = Country.search([], limit=5)
            address, = Address.create([{
                'party': party,
                'name': 'Name',
                'street': 'Street',
                'zip': 'zip',
                'city': 'City',
                'country': available_countries[0].id,
                'subdivision':
                    available_countries[0].subdivisions[0].id,
            }])
            self.assertEqual(
                len(current_user.party.payment_profiles), 0)

            with Transaction().set_context({'dummy_succeed': True}):
                # request to add credit card with invalid address
                rv = c.post(
                    '/en/my-cards/add-card',
                    data={
                        'owner': 'Test User',
                        'number': '4111111111111111',
                        'expiry_month': '01',
                        'expiry_year': '2018',
                        'cvv': '111',
                        'address': 123,
                    }
                )
            self.assertTrue(
                'Address you selected is not valid.'
                in rv.data.decode('utf-8'))

    @with_transaction()
    def test_0050_remove_payment_profile(self):
        """
        Test to deactivate the payment profile when the user wants
        to remove it.
        """
        pool = Pool()
        Party = pool.get('party.party')
        Address = pool.get('party.address')
        Country = pool.get('country.country')
        Company = pool.get('company.company')
        NereidUser = pool.get('nereid.user')
        Website = pool.get('nereid.website')
        Profile = pool.get('party.payment_profile')
        Gateway = pool.get('payment_gateway.gateway')
        Journal = pool.get('account.journal')

        create_website()
        app = self.get_app()

        # Create test users
        party, = Party.create([{
            'name': 'Registered User',
        }])
        company, = Company.search([])
        registered_user, = NereidUser.create([{
            'party': party,
            'name': 'Registered User',
            'email': 'email@example.com',
            'password': 'password',
            'company': company,
        }])
        # Define a new payment gateway
        gateway = create_payment_gateway(method='dummy')
        website, = Website.search([])
        website.credit_card_gateway = gateway
        website.save()

        with app.test_client() as c:
            response = c.post(
                '/en/login',
                data={
                    'email': 'email@example.com',
                    'password': 'password',
                    }
                )
            self.assertEqual(response.status_code, 302)  # Login success

            create_countries()
            available_countries = Country.search([], limit=5)
            address, = Address.create([{
                'party': party,
                'name': 'Name',
                'street': 'Street',
                'zip': 'zip',
                'city': 'City',
                'country': available_countries[0].id,
                'subdivision':
                    available_countries[0].subdivisions[0].id,
            }])
            self.assertEqual(
                len(current_user.party.payment_profiles), 0)

            profile1, = Profile.create([{
                'last_4_digits': '1111',
                'sequence': '10',
                'expiry_month': '01',
                'expiry_year': '2018',
                'address': address.id,
                'party': current_user.party.id,
                'provider_reference': '27478839|25062702',
                'gateway': gateway.id,
            }])

            profile2, = Profile.create([{
                'last_4_digits': '1131',
                'sequence': '10',
                'expiry_month': '02',
                'expiry_year': '2018',
                'address': address.id,
                'party': current_user.party.id,
                'provider_reference': '27478839|25062710',
                'gateway': gateway.id,
            }])

            self.assertEqual(
                len(current_user.party.payment_profiles), 2)

            with Transaction().set_context({'dummy_succeed': True}):
                rv = c.post(
                    '/en/my-cards/remove-card',
                    data={
                        'profile_id':
                        current_user.party.payment_profiles[0].id,
                    }
                )

                self.assertEqual(rv.status_code, 302)
                self.assertEqual(
                    len(current_user.party.payment_profiles), 1)

                # Remove payment profile by xhr request
                rv = c.post(
                    '/en/my-cards/remove-card',
                    data={
                        'profile_id':
                        current_user.party.payment_profiles[0].id,
                    }, headers=[('X-Requested-With', 'XMLHttpRequest')]
                )
                self.assertEqual(rv.status_code, 200)
                self.assertEqual(
                    len(current_user.party.payment_profiles), 0)

    @with_transaction()
    def test_0060_remove_invalid_payment_profile(self):
        """
        Test to check if payment profile user wants to remove is valid.
        """
        pool = Pool()
        Party = pool.get('party.party')
        Address = pool.get('party.address')
        Country = pool.get('country.country')
        Company = pool.get('company.company')
        NereidUser = pool.get('nereid.user')
        Website = pool.get('nereid.website')
        Profile = pool.get('party.payment_profile')
        Gateway = pool.get('payment_gateway.gateway')
        Journal = pool.get('account.journal')

        create_website()
        app = self.get_app()

        # Create test users
        party, = Party.create([{
            'name': 'Registered User',
        }])
        company, = Company.search([])
        registered_user, = NereidUser.create([{
            'party': party,
            'name': 'Registered User',
            'email': 'email@example.com',
            'password': 'password',
            'company': company,
        }])
        # Define a new payment gateway
        gateway = create_payment_gateway(method='dummy')
        website, = Website.search([])
        website.credit_card_gateway = gateway
        website.save()

        with app.test_client() as c:
            response = c.post(
                '/en/login',
                data={
                    'email': 'email@example.com',
                    'password': 'password',
                    }
                )
            self.assertEqual(response.status_code, 302)  # Login success

            create_countries()
            available_countries = Country.search([], limit=5)
            address, = Address.create([{
                'party': party,
                'name': 'Name',
                'street': 'Street',
                'zip': 'zip',
                'city': 'City',
                'country': available_countries[0].id,
                'subdivision':
                    available_countries[0].subdivisions[0].id,
            }])
            self.assertEqual(
                len(current_user.party.payment_profiles), 0)

            profile1, = Profile.create([{
                'last_4_digits': '1111',
                'sequence': '10',
                'expiry_month': '01',
                'expiry_year': '2018',
                'address': address.id,
                'party': current_user.party.id,
                'provider_reference': '27478839|25062702',
                'gateway': gateway.id,
            }])

            self.assertEqual(
                len(current_user.party.payment_profiles), 1)

            with Transaction().set_context({'dummy_succeed': True}):
                rv = c.post(
                    '/en/my-cards/remove-card',
                    data={
                        'profile_id': 123,
                    })

                self.assertEqual(rv.status_code, 403)
                self.assertEqual(
                    len(current_user.party.payment_profiles), 1)


def suite():
    suite = test_suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
            NereidPaymentGatewayTestCase))
    return suite
