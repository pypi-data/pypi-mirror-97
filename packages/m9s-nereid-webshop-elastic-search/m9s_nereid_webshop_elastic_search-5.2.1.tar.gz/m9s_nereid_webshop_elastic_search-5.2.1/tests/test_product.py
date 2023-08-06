# -*- coding: utf-8 -*-
"""
    tests/test_product.py

"""
import unittest
import time
import datetime
from dateutil.relativedelta import relativedelta
from decimal import Decimal
from pyes.managers import Indices

import trytond.tests.test_tryton
from trytond.tests.test_tryton import POOL, USER, CONTEXT, with_transaction
from trytond.transaction import Transaction
from nereid.testing import NereidTestCase


class TestProduct(NereidTestCase):
    "Test Product"

    def setUp(self):
        """
        Set up data used in the tests.
        this method is called before each test function execution.
        """
        trytond.tests.test_tryton.install_module(
            'nereid_webshop_elastic_search'
        )

        self.ProductTemplate = POOL.get('product.template')
        self.Uom = POOL.get('product.uom')
        self.ProductCategory = POOL.get('product.category')
        self.Product = POOL.get('product.product')
        self.IndexBacklog = POOL.get('elasticsearch.index_backlog')
        self.PriceList = POOL.get('product.price_list')
        self.Party = POOL.get('party.party')
        self.Company = POOL.get('company.company')
        self.User = POOL.get('res.user')
        self.Currency = POOL.get('currency.currency')
        self.FiscalYear = POOL.get('account.fiscalyear')
        self.Account = POOL.get('account.account')
        self.PaymentTerm = POOL.get('account.invoice.payment_term')
        self.Sale = POOL.get('sale.sale')
        self.Language = POOL.get('ir.lang')
        self.NereidWebsite = POOL.get('nereid.website')
        self.SaleChannel = POOL.get('sale.channel')
        self.Country = POOL.get('country.country')
        self.Subdivision = POOL.get('country.subdivision')
        self.NereidUser = POOL.get('nereid.user')
        self.Location = POOL.get('stock.location')
        self.Locale = POOL.get('nereid.website.locale')
        self.Node = POOL.get('product.tree_node')
        self.ElasticConfig = POOL.get('elasticsearch.configuration')
        self.ElasticDocumentType = POOL.get('elasticsearch.document.type')
        self.ProductAttribute = POOL.get('product.attribute')
        self.ProductAttributeSet = POOL.get('product.attribute.set')

        self.templates = {
            'search-results.jinja': '''
                {% for product in products %}
                {{ product.name }}
                {{ product.code }}
                {% endfor %}
            ''',
        }

    def create_products(self):
        """
        Returns two products
        """
        category, = self.ProductCategory.create([{
            'name': 'Test Category',
            'accounting': True,
        }])
        uom, = self.Uom.search([('symbol', '=', 'u')])

        self.template1, self.template2, self.template3, self.template4, \
            self.template5, self.template6 = \
            self.ProductTemplate.create([
                {
                    'name': 'Prøduçt 1 ünîçø∂e',
                    'type': 'goods',
                    'categories': [('add', [category.id])],
                    'account_category': category.id,
                    'default_uom': uom.id,
                    'description': 'This is product 1',
                    'list_price': 5000,
                    'cost_price': 4000,
                },
                {
                    'name': 'Product 2',
                    'type': 'goods',
                    'categories': [('add', [category.id])],
                    'account_category': category.id,
                    'default_uom': uom.id,
                    'description': 'This is product 2',
                    'list_price': 3000,
                    'cost_price': 2000,
                },
                {
                    'name': 'ActiveProduct',
                    'type': 'goods',
                    'categories': [('add', [category.id])],
                    'account_category': category.id,
                    'default_uom': uom.id,
                    'description':
                        'This is product for active testing',
                    'list_price': 3000,
                    'cost_price': 2000,
                },
                {
                    'name': 'DisplayProduct',
                    'type': 'goods',
                    'categories': [('add', [category.id])],
                    'account_category': category.id,
                    'default_uom': uom.id,
                    'description': 'This is product for e-shop display testing',
                    'list_price': 3000,
                    'cost_price': 2000,
                },
                {
                    'name': 'InactiveProduct',
                    'type': 'goods',
                    'categories': [('add', [category.id])],
                    'account_category': category.id,
                    'default_uom': uom.id,
                    'description': 'This is product for inactive testing',
                    'list_price': 3000,
                    'cost_price': 2000,
                },
                {
                    'name': 'NotDisplayProduct',
                    'type': 'goods',
                    'categories': [('add', [category.id])],
                    'account_category': category.id,
                    'default_uom': uom.id,
                    'description': 'This is product for non-display testing',
                    'list_price': 3000,
                    'cost_price': 2000,
                },
            ])

        return self.Product.create([
            {
                'template': self.template1,
                'code': 'code1',
                'displayed_on_eshop': True,
                'uri': 'prod1',
            },
            {
                'template': self.template2,
                'code': 'code of product 2',
                'displayed_on_eshop': True,
                'uri': 'prod2',
            },
            {
                'template': self.template3,
                'code': 'code of activeproduct',
                'displayed_on_eshop': True,
                'uri': 'activeprod',
            },
            {
                'template': self.template4,
                'code': 'code of displayproduct',
                'displayed_on_eshop': True,
                'uri': 'displayprod',
            },
            {
                'template': self.template5,
                'code': 'code of inactiveproduct',
                'active': False,
                'displayed_on_eshop': True,
                'uri': 'inactiveprod',
            },
            {
                'template': self.template6,
                'code': 'code of notdisplayproduct',
                'displayed_on_eshop': False,
                'uri': 'notdisplayprod',
            },
        ])

    def _create_fiscal_year(self, date=None, company=None):
        """
        Creates a fiscal year and requried sequences
        """
        Sequence = POOL.get('ir.sequence')
        SequenceStrict = POOL.get('ir.sequence.strict')

        if date is None:
            date = datetime.date.today()

        if company is None:
            company, = self.Company.search([], limit=1)

        invoice_sequence, = SequenceStrict.create([{
            'name': '%s' % date.year,
            'code': 'account.invoice',
            'company': company,
        }])
        fiscal_year, = self.FiscalYear.create([{
            'name': '%s' % date.year,
            'start_date': date + relativedelta(month=1, day=1),
            'end_date': date + relativedelta(month=12, day=31),
            'company': company,
            'post_move_sequence': Sequence.create([{
                'name': '%s' % date.year,
                'code': 'account.move',
                'company': company,
            }])[0],
            'out_invoice_sequence': invoice_sequence,
            'in_invoice_sequence': invoice_sequence,
            'out_credit_note_sequence': invoice_sequence,
            'in_credit_note_sequence': invoice_sequence,
        }])
        self.FiscalYear.create_period([fiscal_year])
        return fiscal_year

    def _create_coa_minimal(self, company):
        """Create a minimal chart of accounts
        """
        AccountTemplate = POOL.get('account.account.template')
        account_create_chart = POOL.get(
            'account.create_chart', type="wizard")

        account_template, = AccountTemplate.search([
            ('parent', '=', None),
            ('name', '=', 'Minimal Account Chart')
        ])

        session_id, _, _ = account_create_chart.create()
        create_chart = account_create_chart(session_id)
        create_chart.account.account_template = account_template
        create_chart.account.company = company
        create_chart.transition_create_account()

        receivable, = self.Account.search([
            ('kind', '=', 'receivable'),
            ('company', '=', company),
        ])
        payable, = self.Account.search([
            ('kind', '=', 'payable'),
            ('company', '=', company),
        ])
        create_chart.properties.company = company
        create_chart.properties.account_receivable = receivable
        create_chart.properties.account_payable = payable
        create_chart.transition_create_properties()

    def _create_payment_term(self):
        """Create a simple payment term with all advance
        """

        return self.PaymentTerm.create([{
            'name': 'Direct',
            'lines': [('create', [{'type': 'remainder'}])]
        }])

    def _create_pricelists(self):
        """
        Create the pricelists
        """
        # Setup the pricelists
        self.party_pl_margin = Decimal('1')
        self.guest_pl_margin = Decimal('1')
        user_price_list, = self.PriceList.create([{
            'name': 'PL 1',
            'company': self.company.id,
            'lines': [
                ('create', [{
                    'formula': 'unit_price * %s' % self.party_pl_margin
                }])
            ],
        }])
        guest_price_list, = self.PriceList.create([{
            'name': 'PL 2',
            'company': self.company.id,
            'lines': [
                ('create', [{
                    'formula': 'unit_price * %s' % self.guest_pl_margin
                }])
            ],
        }])
        return guest_price_list.id, user_price_list.id

    def _get_account_by_kind(self, kind, company=None, silent=True):
        """Returns an account with given spec
        :param kind: receivable/payable/expense/revenue
        :param silent: dont raise error if account is not found
        """

        if company is None:
            company, = self.Company.search([], limit=1)

        accounts = self.Account.search([
            ('kind', '=', kind),
            ('company', '=', company)
        ], limit=1)
        if not accounts and not silent:
            raise Exception("Account not found")
        return accounts[0] if accounts else False

    def setup_defaults(self):
        """
        Setup defaults
        """
        usd, = self.Currency.create([{
            'name': 'US Dollar',
            'code': 'USD',
            'symbol': '$',
        }])

        with Transaction().set_context(company=None):
            company_party, = self.Party.create([{
                'name': 'Openlabs',
                'addresses': [('create', [{
                    'name': 'Openlabs',
                }])],
            }])

        self.company, = self.Company.create([{
            'party': company_party.id,
            'currency': usd,
        }])

        self.User.write([self.User(USER)], {
            'company': self.company,
            'main_company': self.company,
        })

        CONTEXT.update(self.User.get_preferences(context_only=True))

        # Create Fiscal Year
        self._create_fiscal_year(company=self.company.id)
        # Create Chart of Accounts
        self._create_coa_minimal(company=self.company.id)
        # Create a payment term
        payment_term, = self._create_payment_term()

        channel_price_list, user_price_list = self._create_pricelists()
        party1, = self.Party.create([{
            'name': 'Guest User',
        }])

        party2, = self.Party.create([{
            'name': 'Registered User',
            'sale_price_list': user_price_list,
        }])

        self.party2 = party2

        party3, = self.Party.create([{
            'name': 'Registered User 2',
        }])

        # Create users and assign the pricelists to them
        self.guest_user, = self.NereidUser.create([{
            'party': party1.id,
            'display_name': 'Guest User',
            'email': 'guest@openlabs.co.in',
            'password': 'password',
            'company': self.company.id,
        }])
        self.registered_user, = self.NereidUser.create([{
            'party': party2.id,
            'display_name': 'Registered User',
            'email': 'email@example.com',
            'password': 'password',
            'company': self.company.id,
        }])
        self.registered_user2, = self.NereidUser.create([{
            'party': party3.id,
            'display_name': 'Registered User 2',
            'email': 'email2@example.com',
            'password': 'password2',
            'company': self.company.id,
        }])

        warehouse, = self.Location.search([
            ('type', '=', 'warehouse')
        ], limit=1)
        location, = self.Location.search([
            ('type', '=', 'storage')
        ], limit=1)
        en_us, = self.Language.search([('code', '=', 'en_US')])

        self.locale_en_us, = self.Locale.create([{
            'code': 'en_US',
            'language': en_us.id,
            'currency': usd.id,
        }])

        with Transaction().set_context({'company': self.company.id}):
            self.channel, = self.SaleChannel.create([{
                'name': 'Default Channel',
                'price_list': channel_price_list,
                'warehouse': warehouse,
                'payment_term': payment_term,
                'create_users': [('add', [USER])],
                'invoice_method': 'order',
                'shipment_method': 'order',
                'source': 'webshop'
            }])
        self.User.set_preferences({'current_channel': self.channel})

        self.User.write(
            [self.User(USER)], {
                'main_company': self.company.id,
                'company': self.company.id,
                'current_channel': self.channel,
            }
        )
        self.default_node, = self.Node.create([{
            'name': 'root',
            'slug': 'root',
        }])
        self.country, = self.Country.create([{
            'name': 'United States',
            'code': 'US',
        }])
        self.subdivision1, = self.Subdivision.create([{
            'country': self.country.id,
            'name': 'California',
            'code': 'US-CA',
            'type': 'state',
        }])
        self.NereidWebsite.create([{
            'name': 'localhost',
            'channel': self.channel,
            'company': self.company.id,
            'application_user': USER,
            'default_locale': self.locale_en_us.id,
            'guest_user': self.guest_user,
            'countries': [('add', [self.country.id])],
            'currencies': [('add', [usd.id])],
        }])

    def clear_server(self):
        """
        Clear the elasticsearch server.
        """
        conn = self.ElasticConfig(1).get_es_connection()
        index_name = self.ElasticConfig(1).get_index_name(name=None)

        indices = Indices(conn)
        indices.delete_index_if_exists(index_name)

    def update_treenode_mapping(self):
        """
        Update tree_nodes mapping as nested.
        """
        product_doc, = self.ElasticDocumentType.search([])
        self.ElasticConfig.update_settings([self.ElasticConfig(1)])
        self.ElasticDocumentType.update_mapping([product_doc])

    @with_transaction()
    def test_0010_test_product_indexing(self):
        """
        Tests indexing on creation and updation of product
        """
        self.update_treenode_mapping()
        self.setup_defaults()

        category_automobile, = self.ProductCategory.create([{
            'name': 'Automobile',
        }])
        uom, = self.Uom.search([('symbol', '=', 'u')])

        template, = self.ProductTemplate.create([{
            'name': 'Bat Mobile',
            'type': 'goods',
            'list_price': 50000,
            'cost_price': 40000,
            'categories': [('add', [category_automobile.id])],
            'default_uom': uom.id,
        }])
        product, = self.Product.create([{
            'template': template,
            'code': 'Batman has a code',
            'use_template_description': False,
            'description': 'This is the BatMobile',
        }])
        self.assertEqual(self.IndexBacklog.search([], count=True), 1)
        # Clear backlog list
        self.IndexBacklog.delete(self.IndexBacklog.search([]))
        self.assertEqual(self.IndexBacklog.search([], count=True), 0)
        # Update the product template
        self.ProductTemplate.write([template], {
            'description': "Batman's ride",
        })
        self.assertEqual(self.IndexBacklog.search([], count=True), 1)

        # Create new products
        self.create_products()

        # Update index on Elastic-Search server
        self.IndexBacklog.update_index()
        time.sleep(2)

        # Test if new records have been uploaded on elastic server
        # If Index Backlog if empty, it means the records got updated
        self.assertEqual(self.IndexBacklog.search([], count=True), 0)

        self.clear_server()

    @with_transaction()
    def test_0020_autocomplete(self):
        """
        Tests the custom autocomplete classmethod
        """
        self.update_treenode_mapping()
        self.setup_defaults()
        self.create_products()
        app = self.get_app()

        self.IndexBacklog.update_index()
        time.sleep(5)

        with app.test_request_context('/'):
            results = self.NereidWebsite.auto_complete('product')

            self.assertIn({
                'display_name': '%s - %s' % (
                    self.template1.products[0].code, self.template1.name
                ),
                'url': self.template1.products[0].get_absolute_url(
                    _external=True
                ),
                'id': self.template1.products[0].id,
                'type': self.template1.type,
            }, results)
            self.assertIn({
                'display_name': '%s - %s' % (
                    self.template2.products[0].code, self.template2.name
                ),
                'url': self.template2.products[0].get_absolute_url(
                    _external=True
                ),
                'id': self.template2.products[0].id,
                'type': self.template2.type,
            }, results)

        self.clear_server()

    @with_transaction()
    def test_0030_product_active_eshop(self):
        """
        Tests for active/inactive and e-shop displayed/hidden products.
        """
        self.update_treenode_mapping()
        self.setup_defaults()
        self.create_products()
        self.IndexBacklog.update_index()
        time.sleep(5)
        app = self.get_app()

        with app.test_client() as c:
            rv = c.get('/search?q=active')
            self.assertIn('Active', rv.data.decode('UTF-8'))

            rv = c.get('/search?q=inactive')
            self.assertNotIn('Inactive', rv.data.decode('UTF-8'))

            rv = c.get('/search?q=display')
            self.assertIn('Display', rv.data.decode('UTF-8'))

            rv = c.get('/search?q=notdisplay')
            self.assertNotIn('NotDisplay', rv.data.decode('UTF-8'))

        self.clear_server()

    @with_transaction()
    def test_0035_search(self):
        """
        Tests product search via elastic search
        """
        self.update_treenode_mapping()
        self.setup_defaults()
        self.create_products()
        self.IndexBacklog.update_index()
        time.sleep(5)
        app = self.get_app()

        with app.test_client() as c:
            rv = c.get('/search?q=product')
            self.assertTrue(self.template2.name in rv.data.decode('UTF-8'))

            rv = c.get('/search?q=test category')
            result = rv.data.decode('UTF-8')
            self.assertTrue(self.template2.name in result)
            self.assertTrue(self.template3.name in result)
            self.assertTrue(self.template4.name in result)

            rv = c.get('/search?q=prøduçt 1 ünîçø∂e')
            self.assertTrue(
                self.template1.name in rv.data.decode('UTF-8')
            )

        self.clear_server()

    @with_transaction()
    def test_0045_product_attributes_indexing(self):
        """
        Test that product attributes are being indexed
        """
        self.update_treenode_mapping()
        self.setup_defaults()

        uom, = self.Uom.search([], limit=1)

        # Create attributes
        attribute1, = self.ProductAttribute.create([{
            'name': 'size',
            'type_': 'selection',
            'display_name': 'Size',
            'selection': [
                ('create', [{
                    'name': 'medium',
                }, {
                    'name': 'large',
                }, {
                    'name': 'extra_large',
                }])
            ]
        }])
        attribute2, = self.ProductAttribute.create([{
            'name': 'color',
            'type_': 'selection',
            'display_name': 'Color',
            'selection': [
                ('create', [{
                    'name': 'blue',
                }, {
                    'name': 'black',
                }])
            ]
        }])
        attribute3, = self.ProductAttribute.create([{
            'name': 'attrib',
            'type_': 'char',
            'display_name': 'Attrib',
        }])
        attribute4, = self.ProductAttribute.create([{
            'name': 'ø',
            'type_': 'char',
            'display_name': 'ø',
        }])

        # Create attribute set
        attrib_set, = self.ProductAttributeSet.create([{
            'name': 'Cloth',
            'attributes': [
                ('add', [attribute1.id, attribute2.id, attribute4.id])
            ],
        }])

        # Create product template with attribute set
        template1, = self.ProductTemplate.create([{
            'name': 'This is Product',
            'type': 'goods',
            'list_price': Decimal('10'),
            'cost_price': Decimal('5'),
            'default_uom': uom.id,
            'attribute_set': attrib_set.id,
        }])

        product1, = self.Product.create([{
            'template': template1.id,
            'displayed_on_eshop': True,
            'uri': 'uri3',
            'code': 'SomeProductCode',
            'attributes': [
                ('create', [{
                    'attribute': attribute1.id,
                    'value_selection': attribute1.selection[0].id,
                }, {
                    'attribute': attribute2.id,
                    'value_selection': attribute2.selection[0].id,
                }, {
                    'attribute': attribute4.id,
                    'value_char': 'Test Char Value',
                }])
            ],
        }])

        self.assertEqual(self.IndexBacklog.search([], count=True), 1)

        self.IndexBacklog.update_index()
        time.sleep(2)

        self.assertEqual(self.IndexBacklog.search([], count=True), 0)

        self.clear_server()

    @with_transaction()
    def test_0050_filtering(self):
        """
        Test whether filtering works.
        """
        self.update_treenode_mapping()
        self.setup_defaults()
        app = self.get_app()

        uom, = self.Uom.search([], limit=1)

        # Create attributes
        # By default, `filterable` is True.
        attribute1, = self.ProductAttribute.create([{
            'name': 'size',
            'type_': 'selection',
            'display_name': 'Size',
            'selection': [
                ('create', [{
                    'name': 'medium',
                }, {
                    'name': 'large',
                }, {
                    'name': 'extra_large',
                }])
            ]
        }])
        attribute2, = self.ProductAttribute.create([{
            'name': 'color',
            'type_': 'selection',
            'display_name': 'Color',
            'selection': [
                ('create', [{
                    'name': 'blue',
                }, {
                    'name': 'black',
                }])
            ]
        }])
        attribute3, = self.ProductAttribute.create([{
            'name': 'medium',
            'type_': 'selection',
            'display_name': 'Medium',
            'selection': [
                ('create', [{
                    'name': 'digital',
                }, {
                    'name': 'physical',
                }])
            ]
        }])

        # Create attribute set
        attrib_set, = self.ProductAttributeSet.create([{
            'name': 'Cloth',
            'attributes': [
                ('add', [attribute1.id, attribute2.id, attribute3.id])
            ]
        }])

        # Create product template with attribute set
        template1, = self.ProductTemplate.create([{
            'name': 'This is Product',
            'type': 'goods',
            'list_price': Decimal('10'),
            'cost_price': Decimal('5'),
            'default_uom': uom.id,
            'attribute_set': attrib_set.id,
        }])

        product1, = self.Product.create([{
            'template': template1.id,
            'displayed_on_eshop': True,
            'uri': 'uri1',
            'code': 'SomeProductCode1',
            'attributes': [
                ('create', [{
                    'attribute': attribute1.id,  # size
                    'value_selection': attribute1.selection[2].id,  # XL
                }, {
                    'attribute': attribute3.id,  # medium
                    'value_selection': attribute3.selection[0].id,  # digi
                }])
            ],
        }])

        product2, = self.Product.create([{
            'template': template1.id,
            'displayed_on_eshop': True,
            'uri': 'uri2',
            'code': 'SomeProductCode2',
            'attributes': [
                ('create', [{
                    'attribute': attribute2.id,  # color
                    'value_selection': attribute2.selection[1].id,  # black
                }, {
                    'attribute': attribute1.id,  # size
                    'value_selection': attribute1.selection[1].id,  # large
                }, {
                    'attribute': attribute3.id,  # medium
                    'value_selection': attribute3.selection[0].id,  # digi
                }])
            ],
        }])

        product3, = self.Product.create([{
            'template': template1.id,
            'displayed_on_eshop': True,
            'uri': 'uri3',
            'code': 'SomeProductCode3',
            'attributes': [
                ('create', [{
                    'attribute': attribute2.id,  # color
                    'value_selection': attribute2.selection[0].id,  # blue
                }, {
                    'attribute': attribute3.id,  # medium
                    'value_selection': attribute3.selection[1].id,  # phys
                }])
            ],
        }])

        self.IndexBacklog.update_index()
        time.sleep(2)

        with app.test_client() as c:
            # No result search
            rv = c.get('/search?q=NotHere&color=black&size=xl')
            self.assertEqual(rv.data.strip(), '')

            # Color should be black
            rv = c.get('/search?q=product&color=black')
            self.assertTrue(product2.code in rv.data)
            self.assertFalse(product3.code in rv.data)

            # Color could be blue or black
            rv = c.get('/search?q=product&color=blue&color=black')
            self.assertTrue(product2.code in rv.data)
            self.assertTrue(product3.code in rv.data)

            # Color should be blue or black and the medium should be
            # physical
            rv = c.get(
                '/search?q=product&color=blue&color=black&medium=physical'
            )
            self.assertTrue(product3.code in rv.data)
            self.assertFalse(product1.code in rv.data)
            self.assertFalse(product2.code in rv.data)

            # Medium should be digital
            rv = c.get('/search?q=product&medium=digital')
            self.assertTrue(product1.code in rv.data)
            self.assertTrue(product2.code in rv.data)

        # Now test that the facet tallies get updated due to filtering.
        # First, no filtering case.
        with app.test_request_context('/search?q=product'):
            facets = self.NereidWebsite.quick_search().context['facets']

            self.assertItemsEqual(
                facets['color']['terms'],
                [
                    {'count': 1, 'term': 'blue'},
                    {'count': 1, 'term': 'black'}
                ]
            )
            self.assertItemsEqual(
                facets['medium']['terms'],
                [
                    {'count': 2, 'term': 'digital'},
                    {'count': 1, 'term': 'physical'}
                ]
            )
            self.assertItemsEqual(
                facets['size']['terms'],
                [
                    {'count': 1, 'term': 'extra_large'},
                    {'count': 1, 'term': 'large'},
                ]
            )

        # Apply a filter.
        with app.test_request_context('/search?q=product&color=black'):
            facets = self.NereidWebsite.quick_search().context['facets']
            self.assertItemsEqual(
                facets['color']['terms'],
                [
                    {'count': 1, 'term': 'black'},
                    {'count': 0, 'term': 'blue'},
                ]
            )
            self.assertItemsEqual(
                facets['medium']['terms'],
                [
                    {'count': 1, 'term': 'digital'},
                    {'count': 0, 'term': 'physical'},
                ]
            )
            self.assertItemsEqual(
                facets['size']['terms'],
                [
                    {'count': 1, 'term': 'large'},
                    {'count': 0, 'term': 'extra_large'},
                ]
            )


def suite():
    """
    Define suite
    """
    test_suite = trytond.tests.test_tryton.suite()
    test_suite.addTests(
        unittest.TestLoader().loadTestsFromTestCase(TestProduct)
    )
    return test_suite

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
